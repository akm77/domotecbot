from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence, Dict, List, Any

from aiogram.types import User
from charset_normalizer.md import Optional
from sqlalchemy import Result, select, func, update
from sqlalchemy.dialects.sqlite import insert, Insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgbot.models.costing_data import User as DBUser


def get_upsert_user_query(values) -> Insert:
    insert_statement = insert(DBUser).values(values)
    update_statement = insert_statement.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(is_bot=insert_statement.excluded.is_bot,
                  first_name=insert_statement.excluded.first_name,
                  last_name=insert_statement.excluded.last_name,
                  username=insert_statement.excluded.username,
                  language_code=insert_statement.excluded.language_code,
                  is_premium=insert_statement.excluded.is_premium)).returning(DBUser)
    return update_statement


async def upsert_user_from_middleware(session: async_sessionmaker, user: User) -> Optional[DBUser]:
    # id: Mapped[int] = mapped_colu-mn(primary_key=True)
    # is_bot: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
    # first_name: Mapped[str] = mapped_column(nullable=False)
    # last_name: Mapped[str] = mapped_column(nullable=True)
    # username: Mapped[str] = mapped_column(nullable=True)
    # lang_code: Mapped[str] = mapped_column(nullable=True, server_default=text("ru_RU"))
    # is_premium: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
    # role: Mapped[str] = mapped_column(String(length=100), server_default=text("user"))
    async with session() as session:
        result: Result = await session.execute(get_upsert_user_query({"id": user.id,
                                                                      "is_bot": user.is_bot,
                                                                      "first_name": user.first_name,
                                                                      "last_name": user.last_name,
                                                                      "username": user.username,
                                                                      "language_code": user.language_code,
                                                                      "is_premium": user.is_premium if user.is_premium
                                                                      else False}))
        await session.commit()
        return result.scalars().one_or_none()


@dataclass
class Component:
    type: str
    name: str
    media: str
    description: str


FOUNDATIONS = {"type-1": Component(type="type-1",
                                   name="Свайно-винтовой",
                                   media="tgbot/media/fnd_type-1.png",
                                   description="""\
<b>Свайно-винтовой фундамент</b> состоит из стальных опор, заглубляемых в грунт посредством вкручивания ручным или 
механизированным методом. 
Конструкция дополнительно укрепляется ростверком, способствующим равномерному распределению нагрузки."""),
               "type-2": Component(type="type-2",
                                   name="ЖБ сваи",
                                   media="tgbot/media/fnd_type-2.png",
                                   description="""\
<b>Фундамент из забивных железобетонных свай</b> представляет собой готовые свайные столбы, 
забитые на требуемую глубину с помощью специальной техники без предварительной выемки грунта. 
Это удачная альтернатива другим видам основания зданий на сложных грунтах и проблемном рельефе с оврагами, ямами, 
холмами."""),
               "type-3": Component(type="type-3", name="Свайно-ростверковый", media="tgbot/media/fnd_type-3.png",
                                   description="""\
<b>Свайно-ростверковый фундамент</b> – это конструкция из свай, заглубленных в грунт ниже отметки промерзания почвы. 
Его главная черта – они связаны вверху между собой ростверком – железобетонной монолитной плитой. 
Такой фундамент еще называют столбчато-ленточным. 
Он подходит даже для мягких и подвижных почв, песчаных или глинистых участков со значительными рельефными 
перепадами."""),
               "type-4": Component(type="type-4", name="Монолитная плита", media="tgbot/media/fnd_type-4.png",
                                   description="""\
<b>Фундамент на основе монолитной плиты</b> – это сплошная монолитная железобетонная плита, 
уложенная под всю площадь будущего дома. 
Главная отличительная особенность этого типа фундамента от всех других – наибольшая опорная площадь, 
которая позволяет обеспечить высокие показатели устойчивости будущего строения.""")}


def get_foundations():
    return FOUNDATIONS.values()


def get_foundation(key: str):
    return FOUNDATIONS.get(key)


PARTITION_WALL = Component(type="frame-1",
                           name="Каркасные перегородки из доски",
                           media="tgbot/media/frame-wall.png",
                           description="""\
В качестве основы такой конструкции обычно применяется брус, который впоследствии зашивается доской. 
При этом пространство внутри перегородки заполняется шумоизоляционным материалом, 
таким как минеральная вата, эковата и пр.                               
                                 """)
WOODEN_I_BEAM = Component(type="ibeam-1",
                          name="Деревянная двутавровая балка",
                          media="tgbot/media/ibeam-1.png",
                          description="""\
Межэтажная конструкция. С одной стороны балки являются опорным конструктивом для потолка, 
а с другой выступают напольными лагами. 
Межэтажный «пирог» заполняется звуко- и теплоизолятором с применением пароизоляционной прослойки.                              
                                 """)

PARTITIONS = {"sip-1": Component(type="sip-1",
                                 name="Сип-панели ОСП-3",
                                 media="tgbot/media/sip-1.png",
                                 description="""\
Состав: SIP-панель состоит из листов ОСП-3. 
В качестве теплоизоляционного слоя используется пенополистирол ППС14 или ППС16Ф с добавлением антипиренов, 
которые блокируют самостоятельное горение материала.                                 
                                 """),
              "sip-2": Component(type="sip-2",
                                 name="СИП-панели Green Board",
                                 media="tgbot/media/sip-2.png",
                                 description="""\
Состав: СИП панели представляют собой инновационную, экологически чистую, 3-х слойную конструкцию, 
состоящую из двух листов Green Board (GB3) – фибролитовых древесно-цементных плит и твердого пенополистерола ППС 14, 
толщиной 100-200мм.

Green Board (GB3) – фибролитовая древесно-цементная плита состоит из 40% портландцемента М500 и 60% древесной шерсти 
(волокон)                                
                                 """),
              "sip-3": Component(type="sip-3",
                                 name="СИП-панели ЦСП",
                                 media="tgbot/media/sip-3.png",
                                 description="""\
Состав: СИП-панели из ЦСП представляют собой прямоугольные объемные конструкции и состоят из трех слоев:
* два наружных — цементно-стружечные плиты толщиной 10–12 мм;
* внутренний — утеплитель из пенополистирола или минеральной ваты.                                
                                 """)
              }


def get_panel_partitions():
    _d = dict(PARTITIONS)
    return _d.values()


def get_internal_partitions():
    _d = dict(PARTITIONS)
    _d["frame-1"] = PARTITION_WALL
    return _d.values()


def intermediate_floor_partitions():
    _d = dict(PARTITIONS)
    _d["frame-1"] = PARTITION_WALL
    _d["ibeam-1"] = WOODEN_I_BEAM
    _d.pop("sip-1")
    _d.pop("sip-2")
    _d.pop("sip-3")
    return _d.values()


def get_partition(key: str):
    _d = dict(PARTITIONS)
    _d["frame-1"] = PARTITION_WALL
    _d["ibeam-1"] = WOODEN_I_BEAM
    return _d.get(key)


ROOFS = {"slope-1": Component(type="slope-1",
                              name="Крыша в 1 скат",
                              media="tgbot/media/slope-1.png",
                              description="""\
Крыша с одним скатом используется, как навес над хозяйственными постройками или небольшими домами. 
В этом случае имеет небольшой уклон. Часто упирается на несущие стены с разной высотой. 
Сегодня находит применение и при строительстве домов сложной конфигурации многоугольного плана или как решение при \
многоуровневой крыше.                               
                                 """),
         "slope-2": Component(type="slope-2",
                              name="Крыша в 2 ската",
                              media="tgbot/media/slope-2.png",
                              description="""\
Классический вид, наиболее распространенной конструкции крыши. 
Бесчердачная, поскольку здесь перекрытием этажа служат несущие элементы крыши. 
Фронтоны являются продолжением стены строения.                                
                                 """),
         "slope-4": Component(type="slope-4",
                              name="Крыша в 4 ската",
                              media="tgbot/media/slope-4.png",
                              description="""\
Вместо фронтонов крыши расположены треугольные скаты - вальмы. В итоге крышу формируют четыре ската, 
два из которых трапециевидные, два треугольные. Такая крыша более традиционна в южных регионах. 
Монтаж вальмовой крыши отличается сложностью, но с нее легко удаляются осадки и она противостоит ветровой нагрузке.                               
                                 """)}


def get_roofs():
    return ROOFS.values()


def get_roof(key: str):
    return ROOFS.get(key)


ROOF_MATERIALS = {"type-1": Component(type="type-1",
                                      name="Металлочерепица",
                                      media="tgbot/media/rm-1.png",
                                      description="""\
Основой для производства <b>металлочерепицы</b> является тонкая листовая сталь. 
Она прокатывается на специальных станках, делающих из плоского листа рельефное покрытие. 
Причём ребра жёсткости у этого материала имеются не только в продольном направлении, как у профнастила, \
но и в поперечном. 
Последние придают ему визуальную схожесть с черепицей и гораздо большую прочность.
Но стальной лист – это только «сердечник» материала, его несущий каркас, на который с обеих сторон наносятся \
разные виды защитных и декоративных покрытий.
                                 """),
                  "type-2": Component(type="type-2",
                                      name="Профлист",
                                      media="tgbot/media/rm-2.png",
                                      description="""\
<b>Профлист</b> - это стальной оцинкованный лист толщиною от 0,35 до 1,2 мм, который формируется путем холодной \
прокатки в материал волнообразного типа. Именно таким способом производится увеличение несущей способности листов. 
При этом форма гофры может быть волнообразной или трапециевидной.
Профлист изготавливается только из оцинкованной стали, у которой высокие влагозащитные свойства, \
противостоящие процессам коррозии металлов, плюс увеличивающие срок эксплуатации материала
                                 """),
                  "type-3": Component(type="type-3",
                                      name="Мягкая кровля",
                                      media="tgbot/media/rm-3.png",
                                      description="""\
<b>Мягкая кровля</b> производится на основе стеклохолста или другого прочного материала. 
Как и на сталь, на него с обеих сторон наносится защитный и укрепляющий слой битума, модифицированного полимерными \
добавками, обеспечивающими полотну гибкость и устойчивость к температурным перепадам.
Снизу есть ещё один битумный слой, самоклеящийся, закрытый защитной плёнкой. 
А сверху черепица покрыта декоративным слоем из сланцевой, базальтовой или кремниевой крошки. 
Как любой природный материал, она отличается неоднородностью цвета, что и делает гибкую черепицу так \
похожей на натуральную керамическую.
                                 """),
                  "type-4": Component(type="type-4",
                                      name="Наплавляемая кровля",
                                      media="tgbot/media/rm-4.png",
                                      description="""\
<b>Наплавляемая кровля</b> – разновидность мягкой рулонной битумной гидроизоляции, предназначенная для покрытия \
эксплуатируемых и неэксплуатируемых крыш плоских или с небольшим уклоном методом наплавления пламенем газовой горелки.
                                 """),
                  "type-5": Component(type="type-5",
                                      name="ПВХ-кровля",
                                      media="tgbot/media/rm-5.png",
                                      description="""\
<b>ПВХ-кровля</b> – это однослойный вид кровли, который изготавливается на основе эластичного поливинилхлорида (PVC-P). 
Сварка горячим воздухом, которой подвергается мембранная кровля из ПВХ, \
обеспечивает материалу целостность поверхности и абсолютную герметичность.                              
                                 """)}


def get_roof_materials():
    return ROOF_MATERIALS.values()


def get_roof_material(key: str):
    return ROOF_MATERIALS.get(key)


@dataclass
class Element:
    code: str
    name: str


ESTIMATE_TYPES = {"construct": Element(code="construct", name="Строительство"),
                  "house_kit": Element(code="house_kit", name="Домокомплект")}


def get_estimate_types():
    return ESTIMATE_TYPES.values()


def get_estimate_type(key: str):
    return ESTIMATE_TYPES.get(key)
