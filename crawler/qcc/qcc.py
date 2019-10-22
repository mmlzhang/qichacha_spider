
import re
import scrapy

from bigcrawler.crawler import BaseSpider


class QccSpider(BaseSpider):
    name = "qichacha"

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS": 1,
        "DEPTH_PRIORITY": 1,
        "PROXIES": {}
    }

    domain = 'https://www.qichacha.com'
    # start_urls = ["https://www.qichacha.com/g_BJ"]
    page_reg = re.compile(r'\S+?prov=(\S+?)&p=(\d+)')

    def start_requests(self):
        province_map = {
            '上海': '/g_SH.html',
            '云南': '/g_YN.html',
            '内蒙古': '/g_NMG.html',
            '吉林': '/g_JL.html',
            '四川': '/g_SC.html',
            '天津': '/g_TJ.html',
            '宁夏': '/g_NX.html',
            '安徽': '/g_AH.html',
            '山东': '/g_SD.html',
            '山西': '/g_SX.html',
            '广东': '/g_GD.html',
            '广西': '/g_GX.html',
            '新疆': '/g_XJ.html',
            '江苏': '/g_JS.html',
            '江西': '/g_JX.html',
            '河北': '/g_HB.html',
            '河南': '/g_HEN.html',
            '浙江': '/g_ZJ.html',
            '海南': '/g_HAIN.html',
            '湖北': '/g_HUB.html',
            '湖南': '/g_HUN.html',
            '甘肃': '/g_GS.html',
            '福建': '/g_FJ.html',
            '西藏': '/g_XZ.html',
            '贵州': '/g_GZ.html',
            '辽宁': '/g_LN.html',
            '重庆': '/g_CQ.html',
            '陕西': '/g_SAX.html',
            '青海': '/g_QH.html',
            '黑龙江': '/g_HLJ.html'
        }
        for province, uri in province_map.items():
            url = self.domain + uri
            yield scrapy.Request(url)

    def parse(self, response):
        # 所有省地区
        provinces = response.xpath('//a[@class="pills-item "]')
        for province in provinces:
            href = province.xpath("./@href").extract()[0]
            name = province.xpath("./text()").extract()[0]
            if "-" not in name:
                print(href, name)
                next_url = self.domain + href
                yield scrapy.Request(next_url, callback=self.parse_list)

    def parse_list(self, response):
        company_list = response.xpath("//a[@class='ma_h1']")
        for company in company_list:
            href = company.xpath("./@href").extract()[0]
            name = company.xpath("./text()").extract()[0]
            print(href, name)
            url = self.domain + href
            yield scrapy.Request(url, callback=self.parse_detail)

        next_url = response.css(".next::attr(href)").extract_first()
        if next_url:
            if not next_url.startswith(self.domain):
                next_url = self.domain + next_url
            reg_groups = self.page_reg.match(next_url)
            if reg_groups:
                # 下一页
                yield scrapy.Request(next_url, callback=self.parse_list)

    def parse_detail(self, response):
        company_name = response.xpath('//*[@id="company-top"]/div[2]/div[2]/div[1]/h1/text()').extract_first()
        keys = ["名称",'法定代表人', '注册资本', '实缴资本', '经营状态', '成立日期', '统一社会信用代码', '纳税人识别号', '注册号',
                '组织机构代码', '企业类型', '所属行业', '核准日期', '登记机关', '所属地区', '英文名', '曾用名', '参保人数',
                '人员规模', '营业期限', '企业地址', '经营范围', "股东信息", "主要人员", "url"]
        company_detail = {"名称": company_name, "url": response.url}
        if not response.text.startswith('<script>'):
            pass
        else:
            # 工商信息
            td_list = response.xpath("//section[@class='panel b-a base_info']/table[@class='ntable']/tr/td")
            key = ""
            for i, td in enumerate(td_list):
                text = td.xpath(".//text()")
                if i < 2:
                    text = "".join(text.extract())
                else:
                    text = text.extract_first()
                text = re.sub(r"[\r\n\s]+", "", text)
                if text in keys:
                    key = text
                if key:
                    company_detail[key] = text

            # 股东信息
            tr_list = response.xpath("//table[@class='ntable ntable-odd npth nptd']/tr")
            shareholder_info = []
            for tr in tr_list[1:]:
                # 股东
                shareholder = tr.xpath(".//h3[@class='seo font-14']//text()").extract_first().strip()
                # 持股比例
                hold_ratio = tr.xpath(".//td[@class='text-center']/text()").extract_first().strip()
                # 认缴出资额(万元)
                money = tr.xpath(".//td[@class='text-center'][2]/text()").extract_first().strip() + "万"
                # 认缴出资日期
                date = tr.xpath(".//td[@class='text-center'][3]/text()").extract_first().strip()
                shareholder_info.append({
                    "股东": shareholder,
                    "持股比例": hold_ratio,
                    "认缴出资额": money,
                    "认缴出资日期": date,
                })
            company_detail["股东信息"] = shareholder_info

            # 主要人员
            main_staff = []
            tr_list = response.xpath("//table[@class='ntable ntable-odd']//tr")
            for tr in tr_list[1:]:
                name = tr.xpath(".//h3[@class='seo font-14']//text()").extract_first().strip()
                # 职务
                duty = tr.xpath(".//td[@class='text-center']/text()").extract_first().strip()
                main_staff.append({
                    "姓名": name,
                    "职务": duty
                })
            company_detail["主要人员"] = main_staff
        yield self.make_item(filename="qcc_company_detail", data=company_detail, headers=keys)
