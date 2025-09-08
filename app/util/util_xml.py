import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def extract_product_detail_urls_from_xml(xml_file_path: str) -> set[str]:
    product_urls = set()

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        for url in root.findall("sitemap:url", namespace):
            loc_element = url.find("sitemap:loc", namespace)
            if loc_element is not None and loc_element.text:
                if "/product/detail/" in loc_element.text:
                    product_urls.add(loc_element.text)

        return product_urls

    except ET.ParseError as e:
        logger.error("XML 파싱 오류:", e)
        raise
    except FileNotFoundError as e:
        logger.error("파일을 찾을 수 없습니다:", xml_file_path, e)
        raise
    except Exception as e:
        logger.error("예상치 못한 오류 발생으로 확인이 필요합니다:", e)
        raise
