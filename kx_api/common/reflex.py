#__coding__:'utf-8'
#auther:ly
from kx_api.common.my_config import MyConfig
import random
import datetime

class Reflex:
    '''反射类,实现对动态参数值修改、赋值、删除的操作'''
    #header用来存取web端，pos端登陆后token信息
    header = {
        'Content-Type': 'application/json;charset=utf-8',
    }

    #公司编号和租户id
    TenancyName = MyConfig().get_string('base','TenancyName')
    # 获取新增店铺，新增pos，绑定pos需要的参数值
    BStoreCode = MyConfig().get_string('Bind', 'BStoreCode')  # 店铺编码 新增传入
    BPosCode = MyConfig().get_string('Bind', 'BPosCode')  # 新增pos编码
    storeName = MyConfig().get_string('Bind', 'storeName')  # 新增店铺名称
    MachineMac = MyConfig().get_string('Bind', 'MachineMac')
    MachineName = MyConfig().get_string('Bind', 'MachineName')
    Platform = MyConfig().get_string('Bind', 'Platform')  # 平台1表示pos 2表示安卓

    # 新增店铺，新增pos，新增营业员，绑定pos，获取id，pos id，营业员id，pos绑定id
    StoreId = None
    PosId = None
    ClientPosBindId = None
    TenantId = None



    #新增商品分类
    atproductcatecarycode = MyConfig().get_string('atproductcatecary', 'atproductcatecarycode')
    atproductcatecaryname = MyConfig().get_string('atproductcatecary', 'atproductcatecaryname')
    #新增商品分类成功后，获取商品分类id
    productCategoryId = None  # 新增的商品分类id
    productCategoryIdName = None  # 商品分类名称

    # 获取新增商品的编码和名称
    pcode1 = MyConfig().get_string('atproduct', 'pcode1')
    pname1 = MyConfig().get_string('atproduct', 'pname1')

    pcode2 = MyConfig().get_string('atproduct', 'pcode2')
    pname2 = MyConfig().get_string('atproduct', 'pname2')

    pcode3 = MyConfig().get_string('atproduct', 'pcode3')
    pname3 = MyConfig().get_string('atproduct', 'pname3')
    # 创建商品所需要的条形码
    BarCode = None
    #新增的商品id
    productId1 = None
    productId2 = None
    productId3 = None
    #商品3规格主键
    productStandard3Id = None
    productStandard3Name = '罐'
    #商品2规格主键
    productStandard2Id = None
    productStandard2Name = '罐'
    # 商品1规格主键
    productStandard1Id = None
    productStandard1Name = '罐'

    #新增会员卡类型
    cardtypecode = MyConfig().get_string('atcardtype', 'cardtypecode')
    cardtypename = MyConfig().get_string('atcardtype', 'cardtypename')
    #会员卡类型，等级id
    MemberCardTypeId = None
    MemberCardTypeLevelId = None

    #版本号信息
    CurrentVersion = MyConfig().get_string('CurrentVersion','CurrentVersion')  #最新的版本号
    #===================会员模块所需参数===================
    #会员办卡,客户名称、编码、电话号码随机生成5位，也用于新增商品时的商品名称，商品code
    firstname = ['王','刘','左','张','陈','肖']
    x = random.choice(firstname)
    PersonName = x+str(chr(random.randint(0x4e00, 0x9fbf)))
    PersonCode = str(random.randint(0x4e00, 0x9fbf))

    #pos端会员办卡时需要的办卡时间，会员卡类型，等级
    # JoinTime = str(datetime.datetime.now())

    #客户id，会员id
    MemberPersonId = None
    MemberUserId = None
    MemberPersonName = None
    MemberPayId = None
    MemberPayId2 = None
    PersonPhone = None
    PersonPhoneNew = None


    #===========上传账单模块所需的参数=======
    #账单号：读取excel里面的订单号
    BillNumber = None
    #源单单号
    OriginalBillNumber = None
    #单据创建时间
    CreationTime = None
    # #商品分类主键
    # BaseProductCategoryId = None
    # #获取商品id
    # ProductId = None
    # #商品规格主键,获取基础信息时赋值
    # ProductStandardId = None

    #结账方式主键,人名币，会员卡，任我行,抹零，优惠、赠送、免单
    RMBId = None
    MemberCardPayId = None
    GraspPayId = None
    MLPayId = None
    YHPayId = None
    ZSPayId = None
    MDPayId = None

    #任我行支付成功后，返回的数据,商户号，支付通返回的单号,可任意写
    BusinessId = '652711002512500000'
    GraspBillNumberId = None

    # 用户登陆信息pos端登录时的用户名和密码
    UserId = None
    UserName = 'ly'
    Password = '123456'

    #======上传账单 营销方案优惠所需参数(全场8折，果冻特价8元,薯片7折）=======
    AZProjectId = None   #营销方案全场折扣主键
    AZProjectProductCategoryId = None  #营销方案主键对应的商品分类主键
    AZProjectMasterName = '自动新增全场8折'
    #薯片7折
    ZProjectId = None  # 营销方案薯片7折主键
    ZProductStandardId = None  # 薯片商品规格主键
    ZProjectMasterName = '自动新增商品37折'

    TProjectId = None   #营销方案特价主键
    TProductStandardId = None    # 果冻对应的商品规格主键
    TProjectMasterName = '自动新增商品2特价'



    #查询新增成功的商品条码
    LastBarCode = None
    #查询条码库中的商品
    chinaBarCode = None
    #用户班次号excel维护，每次交班后加1
    ShiftKey = None
    LastShiftKey = None


if __name__ == '__main__':

    print(type(Reflex.BillNumber))
    print(Reflex.BillNumber)
    print(Reflex.OriginalBillNumber)
    print(Reflex.TbillNumber)