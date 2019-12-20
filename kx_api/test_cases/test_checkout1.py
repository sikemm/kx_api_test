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
import datetime
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
        # 获取班次号\OrderDetailId
        ShiftKey = self.f.read_tel('ShiftKey')
        LastShiftKey = str(int(ShiftKey) - 1)
        setattr(Reflex, 'ShiftKey', ShiftKey)
        setattr(Reflex, 'LastShiftKey', LastShiftKey)
        # # 获取商品条码
        # BarCode = self.f.read_tel('BarCode')
        # setattr(Reflex, 'BarCode', BarCode)
        # LastBarCode = str(int(BarCode) - 1)
        # setattr(Reflex, 'LastBarCode', LastBarCode)

    def tearDown(self):
        ShiftKeyNew = str(int(getattr(Reflex, 'ShiftKey')) + 1)
        self.f.write_data(2, 1, ShiftKeyNew, 'ShiftKey')
    @data(*test_data)
    def test_checkOut(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        #控制上次账单的条数
        num = int(MyConfig().get_string('number','number'))
        if case['Module'] == 'CheckOut':
            for i in range(num):
                # 获取账单编号，源单号
                BillNumber = self.f.read_tel('billNumber')
                OriginalBillNumber = str(int(BillNumber) - 1)
                setattr(Reflex, 'BillNumber', BillNumber)
                setattr(Reflex, 'GraspBillNumberId', BillNumber)
                setattr(Reflex, 'OriginalBillNumber', OriginalBillNumber)
                #单据创建时间
                now = datetime.datetime.now()
                curr = now.strftime('%Y-%m-%d %H:%M:%S')
                setattr(Reflex,'CreationTime',curr)

                MyLog().info('---=正在执行{0}模块第{1}条测试用例----'.format(case['Module'],i))
                if case['sql'] != None:
                    params1 = re_replace(case['sql'])
                    url1 = 'http://192.168.1.41:11001/api/services/app/Member/MemberPay'
                    resp1 = HttpRequest().http_request('post', url1, params1,getattr(Reflex,'header'))
                    setattr(Reflex, 'MemberPayId', str(resp1.json()['Result']['MemberPayId']))
                # 替换params中的正则参数
                params = re_replace(case['Params'])
                MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))

                #发起请求
                resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
                MyLog().info('ActualResult：{}'.format(resp.text))

                # 每次用例执行完成后，账单编号+1
                billnumber = str(int(getattr(Reflex, 'BillNumber')) + 1)
                self.f.write_data(2, 1, billnumber, 'billNumber')
        else:
            params = re_replace(case['Params'])
            MyLog().info('URL：{0}，Params：{1}'.format(case['url'], params))
            # 发起请求
            resp = HttpRequest().http_request(method, url, params, getattr(Reflex, 'header'))

        try:
            #----------待优化-------
            ActualResult={}
            ActualResult['Success'] = resp.json()['Success']
            self.assertEqual(eval(case['ExpectedResult']), ActualResult)
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



