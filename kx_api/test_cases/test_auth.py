#__coding__:'utf-8'
#auther:ly
import unittest
from ddt import ddt,data
from kx_api.common.do_excel import DoExcel
from kx_api.common import file_path
from kx_api.common.http_request import HttpRequest
from kx_api.common.my_log import MyLog
from kx_api.common.reflex import Reflex
from kx_api.common.re_replace import re_replace,findId

#该模块是用来执行auth表单的测试用例,版本检测、绑定.基础信息获取接口，登录操作

file_name = file_path.api_case_path
sheet_name = 'Auth'
test_data = DoExcel(file_name).read_data(sheet_name)

@ddt
class TestCases(unittest.TestCase):
    '''该类是版本检测、绑定.基础信息、登录模块的测试用例'''
    def setUp(self):
        '''每次用例开始执行前，创建一个读写excel的对象'''
        self.f = DoExcel(file_name)
        BarCode = self.f.read_tel('BarCode')
        setattr(Reflex, 'BarCode', BarCode)

    def tearDown(self):
        BarCodeNew = str(int(getattr(Reflex, 'BarCode')) + 1)
        self.f.write_data(2, 1, BarCodeNew, 'BarCode')

    @data(*test_data)
    def test_auth(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        #替换测试用例中的params的参数,参数为空时不需要替换
        if case['Params'] == None:
            params = case['Params']
        elif case['Method'].upper() == 'POST':
            params = re_replace(case['Params'])
        elif case['Method'].upper() == 'GET':
            params = eval(re_replace(case['Params']))
        MyLog().info('---=正在执行{0}模块第{1}条测试用例:{2}----'.format(case['Module'],case['CaseId'],case['Title']))
        MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))
        resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
        MyLog().info('ActualResult：{}'.format(resp.text))

        #新增店铺、新增pos，绑定pos成功后，获取服务器返回的店铺storeid等,posid, 等注意str的使用，设置时，只能是字符串
        if resp.text.find('businessType') != -1:
            setattr(Reflex, 'StoreId', resp.json()['result']['id'])
        elif resp.text.find('communicationPassword') != -1:
            setattr(Reflex, 'PosId', resp.json()['result']['id'])
        elif resp.text.find('PosId') !=-1:
            setattr(Reflex, 'ClientPosBindId', str(resp.json()['Result']['Id']))
            setattr(Reflex, 'TenantId', str(resp.json()['Result']['TenantId']))


        # 商品分类id，name
        if url.find('BaseProductCategory/Create') !=-1:
            setattr(Reflex, 'productCategoryId', resp.json()['result']['id'])
            setattr(Reflex, 'productCategoryIdName', resp.json()['result']['name'])
        #获取新增商品的id
        if url.find('BaseProduct/Create') !=-1:
            if case['Title'].find('新增商品1') !=-1:
                setattr(Reflex, 'productId1', resp.json()['result']['id'])
                setattr(Reflex, 'productStandard1Id', resp.json()['result']['baseProductStandardList'][0]['baseProductStandardBarCodeList'][0]['baseProductStandardId'])
            elif case['Title'].find('新增商品2') !=-1:
                setattr(Reflex, 'productId2', resp.json()['result']['id'])
                setattr(Reflex, 'productStandard2Id', resp.json()['result']['baseProductStandardList'][0]['baseProductStandardBarCodeList'][0]['baseProductStandardId'])

            elif case['Title'].find('新增商品3') !=-1:
                setattr(Reflex, 'productId3', resp.json()['result']['id'])
                setattr(Reflex, 'productStandard3Id', resp.json()['result']['baseProductStandardList'][0]['baseProductStandardBarCodeList'][0]['baseProductStandardId'])

        #获取会员卡类型id,会员卡等级id
        if url.find('MemberCardType/CreateLevel') != -1:
            setattr(Reflex, 'MemberCardTypeLevelId', resp.json()['result']['id'])
        elif url.find('MemberCardType/Create') !=-1:
            setattr(Reflex, 'MemberCardTypeId', resp.json()['result']['id'])

        #绑定成功后，获取基础信息中的某些参数，用于后续接口使用
        if case['Module'] != 'web' :
            if resp.json()['Success'] == True:
                if url.find('GetBasePaymentWayList') !=-1:
                    # 获取结账方式主键
                    #人民币
                    RMB= findId(resp.json()['Result'],'Code','00001')['Id']
                    setattr(Reflex,'RMBId',str(RMB))
                    #会员卡支付
                    MemberCardPayId = findId(resp.json()['Result'], 'Code', '00003')['Id']
                    setattr(Reflex, 'MemberCardPayId', str(MemberCardPayId))
                    #任我行支付
                    GraspPayId = findId(resp.json()['Result'], 'Code', '00002')['Id']
                    setattr(Reflex, 'GraspPayId', str(GraspPayId))
                    #抹零
                    MLPayId = findId(resp.json()['Result'], 'Code', 'YH001')['Id']
                    setattr(Reflex, 'MLPayId', str(MLPayId))
                    #优惠
                    YHPayId = findId(resp.json()['Result'], 'Code', 'YH002')['Id']
                    setattr(Reflex, 'YHPayId', str(YHPayId))
                    #赠送
                    ZSPayId = findId(resp.json()['Result'], 'Code', 'YH003')['Id']
                    setattr(Reflex, 'ZSPayId', str(ZSPayId))
                    #免单
                    MDPayId = findId(resp.json()['Result'], 'Code', 'YH005')['Id']
                    setattr(Reflex, 'MDPayId', str(MDPayId))
                if url.find('GetUserList') !=-1:
                    # 获取用户信息，取返回的第一个数据
                    UserId = findId(resp.json()['Result'], 'UserName',getattr(Reflex,'UserName') )['Id']
                    setattr(Reflex, 'UserId', str(UserId))
                if url.find('GetProjectMasterList') !=-1:
                    # 营销方案主键数据待增加resp.text.find('全场8折') !=-1:
                    i = findId(resp.json()['Result'], 'Name', '自动新增全场8折2')
                    setattr(Reflex, 'AZProjectId', str(i['Id']))
                    i = findId(resp.json()['Result'], 'Name', '自动新增商品37折2')
                    setattr(Reflex, 'ZProjectId', str(i['Id']))
                    i = findId(resp.json()['Result'], 'Name', '自动新增商品2特价2')
                    setattr(Reflex, 'TProjectId', str(i['Id']))
                if url.find('GetProjectProductStandard4DiscountList') !=-1:
                    # 获取营销方案中商品规格主键
                    #获取折扣商品的商品规格
                    i = findId(resp.json()['Result'], 'ProjectId',int(getattr(Reflex,'ZProjectId')) )
                    setattr(Reflex, 'ZProductStandardId', str(i['ProductStandardId']))
                if url.find('GetProjectProductStandard4SpecialPriceList') !=-1:
                    #获取特价商品的商品规格
                    i = findId(resp.json()['Result'], 'ProjectId', int(getattr(Reflex,'TProjectId')))
                    setattr(Reflex, 'TProductStandardId', str(i['ProductStandardId']))


        # web登录成功后，返回的body里面带有token信息，需要将token信息放在header里面一起请求
        if resp.text.find('accessToken') != -1:
            header = getattr(Reflex, 'header')
            AccessToken = resp.json()['result']['accessToken']
            header['Authorization'] = 'Bearer ' + AccessToken
            setattr(Reflex, 'header', header)
        # pos端登陆成功之后，获取服务器返回的token信息
        elif resp.text.find('AccessToken') != -1:
            header = getattr(Reflex, 'header')
            AccessToken = resp.json()['Result']['AccessToken']
            header['Authorization'] = 'Bearer ' + AccessToken
            setattr(Reflex, 'header', header)
        print(resp.status_code)

        try:
            #----------待优化-------
            ActualResult={}
            if case['Module'] == 'web':
                ActualResult['success'] = resp.json()['success']
                self.assertEqual(eval(case['ExpectedResult']), ActualResult)
            elif case['Module'] == 'GetTenantSetting':
                ActualResult1 = resp.json()['Result'][0]
                self.assertDictContainsSubset(eval(case['ExpectedResult']),ActualResult1)
            elif case['Module'] == 'GetStoreSetting':
                ActualResult1 = resp.json()['Result'][0]
                self.assertDictContainsSubset(eval(case['ExpectedResult']), ActualResult1)
            else:
                ActualResult['Success'] = resp.json()['Success']
                self.assertEqual(eval(case['ExpectedResult']),ActualResult)
            test_result = 'pass'
        except AssertionError as e:
            test_result = 'failed'
            if resp.json()['Error'] != None:
                error_message = resp.json()['Error']['Message']
                MyLog().error('ERROR：{}'.format(error_message))
            MyLog().error('用例执行失败：{}'.format(e))
            raise e
        finally:
            self.f.write_data(case['CaseId']+1,9,resp.text,sheet_name)
            self.f.write_data(case['CaseId']+1,10,test_result,sheet_name)


