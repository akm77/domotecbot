import json
import logging
import shlex
import subprocess
from multiprocessing.dummy import Pool
from queue import Queue
from timeit import default_timer as timer

from vosk import KaldiRecognizer, Model

CHUNK_SIZE = 4000
SAMPLE_RATE = 16000.0

logger = logging.getLogger(__name__)


class Transcriber:

    def __init__(self, model_name: str, lang: str, model_path: str = None):
        self.model = Model(model_path=model_path, model_name=model_name, lang=lang)
        self.queue = Queue()
        self.processed_result = None

    def recognize_stream(self, rec, stream):
        tot_samples = 0
        result = []

        while True:
            data = stream.stdout.read(CHUNK_SIZE)

            if len(data) == 0:
                break

            tot_samples += len(data)
            if rec.AcceptWaveform(data):
                jres = json.loads(rec.Result())
                logger.info(jres)
                result.append(jres)
            else:
                jres = json.loads(rec.PartialResult())
                if jres["partial"] != "":
                    logger.info(jres)

        jres = json.loads(rec.FinalResult())
        result.append(jres)

        return result, tot_samples

    def format_result(self, result, words_per_line=7):
        processed_result = ""
        for part in result:
            if part["text"] != "":
                processed_result += part["text"] + "\n"
        return processed_result

    def resample_ffmpeg(self, infile):
        cmd = shlex.split("ffmpeg -nostdin -loglevel quiet "
                          "-i \'{}\' -ar {} -ac 1 -f s16le -".format(str(infile), SAMPLE_RATE))
        stream = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return stream

    def pool_worker(self, file_name):
        logger.info("Recognizing {}".format(file_name))
        start_time = timer()

        try:
            stream = self.resample_ffmpeg(file_name)
        except FileNotFoundError as e:
            print(e, "Missing FFMPEG, please install and try again")
            return
        except Exception as e:
            logger.info(e)
            return

        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        rec.SetWords(True)
        result, tot_samples = self.recognize_stream(rec, stream)
        if tot_samples == 0:
            return

        self.processed_result = self.format_result(result)
        elapsed = timer() - start_time
        logger.info("Execution time: {:.3f} sec; "
                    "xRT {:.3f}".format(elapsed, float(elapsed) * (2 * SAMPLE_RATE) / tot_samples))

    def process_file(self, file_name):
        self.processed_result = None
        with Pool() as pool:
            pool.map(self.pool_worker, [file_name])
        return self.processed_result
