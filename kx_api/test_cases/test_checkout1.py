#__coding__:'utf-8'
#auther:ly
import unittest
from ddt import ddt,data
from kx_api.common.do_excel import DoExcel
from kx_api.common import file_path
from kx_api.common.http_request import HttpRequest
from kx_api.common.my_log import MyLog
from kx_api.common.reflex import Reflex
from kx_api.common.re_replace import re_replace
from kx_api.common.my_config import MyConfig

#该模块是用来执行checkout表单的测试用例，主要用来新增10万条账单数据

file_name = file_path.api_case_path
sheet_name = 'CheckOut1'
test_data = DoExcel(file_name).read_data(sheet_name)

@ddt
class TestCases(unittest.TestCase):
    '''该类是完成账单和交班模块测试用例  GetBill'''
    def setUp(self):
        '''每次用例开始执行前，创建一个读写excel的对象，读取出上传账单所需要的账单，班次号信息'''
        self.f = DoExcel(file_name)

    def tearDown(self):
        pass
    @data(*test_data)
    def test_checkOut(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        #控制上次账单的条数
        num = int(MyConfig().get_string('number','number'))
        for i in range(num):
            # 获取账单编号，源单号
            BillNumber = self.f.read_tel('billNumber')
            OriginalBillNumber = str(int(BillNumber) - 1)
            setattr(Reflex, 'BillNumber', BillNumber)
            setattr(Reflex, 'GraspBillNumberId', BillNumber)
            setattr(Reflex, 'OriginalBillNumber', OriginalBillNumber)
            # 获取班次号\OrderDetailId
            ShiftKey = self.f.read_tel('ShiftKey')
            LastShiftKey = str(int(ShiftKey) - 1)
            setattr(Reflex, 'ShiftKey', ShiftKey)
            setattr(Reflex, 'LastShiftKey', LastShiftKey)
            # 获取商品条码
            BarCode = self.f.read_tel('BarCode')
            setattr(Reflex, 'BarCode', BarCode)
            LastBarCode = str(int(BarCode) - 1)
            setattr(Reflex, 'LastBarCode', LastBarCode)
            #替换params中的正则参数
            params = re_replace(case['Params'])

            MyLog().info('---=正在执行{0}模块第{1}条测试用例----'.format(case['Module'],i))
            MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))

            #发起请求
            resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
            MyLog().info('ActualResult：{}'.format(resp.text))
            # 每次用例执行完成后，账单编号和班次号+1
            billnumber = str(int(getattr(Reflex, 'BillNumber')) + 1)
            self.f.write_data(2, 1, billnumber, 'billNumber')
            ShiftKeyNew = str(int(getattr(Reflex, 'ShiftKey')) + 1)
            self.f.write_data(2, 1, ShiftKeyNew, 'ShiftKey')

        #交班之后，重新登陆，重新获取token
        if resp.text.find('AccessToken') != -1:
            header = getattr(Reflex, 'header')
            AccessToken = resp.json()['Result']['AccessToken']
            header['Authorization'] = 'Bearer ' + AccessToken
            setattr(Reflex, 'header', header)


        if resp.json()['Success'] == True:
            # 会员支付成功后，获取支付id
            if case['url'].find('MemberPay') != -1:
                setattr(Reflex, 'MemberPayId', str(resp.json()['Result']['MemberPayId']))
            # 执行了创建商品后，商品条码+1
            if url.find('CreateBaseProduct') !=-1:
                BarCodeNew = str(int(getattr(Reflex,'BarCode'))+1)
                self.f.write_data(2,1,BarCodeNew,'BarCode')
        print(resp.status_code)
        try:
            #----------待优化-------
            ActualResult={}

            if case['Module'] == 'GetBill':
                # 获取单个账单
                ActualResult['ClientBillPayDetailList'] = resp.json()['Result']['ClientBillPayDetailList']
                ExpectedResult = eval(re_replace(case['ExpectedResult']))
                self.assertDictEqual(ExpectedResult, ActualResult)
            elif url.find('GetProductInfo') !=-1:
                #获取新增的商品
                if resp.json()['Success'] == True:
                    if resp.json()['Result'] !=None:
                        ActualResult['BarCode'] = resp.json()['Result']['BarCode']
                    else:
                        ActualResult['BarCode'] = None
                else:
                    ActualResult['Success'] = resp.json()['Success']
                ExpectedResult = eval(re_replace(case['ExpectedResult']))
                self.assertDictEqual(ExpectedResult, ActualResult)
            else:
                ActualResult['Success'] = resp.json()['Success']
                self.assertEqual(eval(case['ExpectedResult']),ActualResult)
            test_result = 'pass'
        except AssertionError as e:
            test_result = 'failed'
            if resp.json()['Success'] == False:
                error_message = resp.json()['Error']['Message']
                MyLog().error('ERROR：{}'.format(error_message))
            MyLog().error('用例执行失败：{}'.format(e))
            raise e
        finally:
            self.f.write_data(case['CaseId']+1,9,resp.text,sheet_name)
            self.f.write_data(case['CaseId']+1,10,test_result,sheet_name)



