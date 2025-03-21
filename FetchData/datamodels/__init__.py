from .data_ssq_model import LotterySSQHistory
from .data_kl8_model import LotteryKL8dHistory as LotteryKL8History
from .data_3d_model import Lottery3dHistory as Lottery3DHistory
from.data_super_model import LotterySuperHistory
from.data_p5_model import LotteryP5History

# 添加模型映射关系
MODEL_MAPPING = {
    'ssq': LotterySSQHistory,
    'kl8': LotteryKL8History,
    '3d': Lottery3DHistory,
    'super': LotterySuperHistory,
    'p5': LotteryP5History
}

# 保持原有导入
from .data_ssq_model import *
from .data_kl8_model import *
from .data_3d_model import *
from .data_super_model import *
from .data_p5_model import *