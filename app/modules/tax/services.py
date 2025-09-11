import sys, httpx, traceback
from slugify import slugify
from bs4 import BeautifulSoup


class TaxServices:
    async def _parse_address(self, address: str):
        """
        Parse address into country, province, district, ward. 
        If not detailed enough, still return country + original address.
        """
        results = {"country": "Việt Nam"}
        if not address:
            return results

        # Normalize string
        address = address.replace(".", "").strip()

        if " - " in address:
            details = [part.strip() for part in address.split(" - ")]
        elif "," in address:
            details = [part.strip() for part in address.split(",")]
        else:
            details = [address]

        # Original address (take first 2 parts)
        results["address"] = ", ".join(details[:2])

        # Assign ward, district, province based on length
        n = len(details)
        if n >= 1:
            results["ward"] = details[0].replace(" 0", " ").replace("TP", "Thành phố")
        if n >= 2:
            results["district"] = details[1].replace(" 0", " ").replace("TP", "Thành phố")
        if n >= 3:
            results["province"] = details[2].replace(" 0", " ").replace("TP", "Thành phố")

        return results

    async def _http_get(self, url: str, return_json: bool = False):
        """Helper async GET request"""
        timeout = httpx.Timeout(60.0, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url)
            if return_json:
                return resp.json()
            return resp.text

    async def get_tax_details(self, name: str, tax_code: str):
        results = {}
        try:
            name_slug = slugify(name)
            url = f"https://masothue.com/{tax_code}-{name_slug}"
            response_text = await self._http_get(url)
            soup = BeautifulSoup(response_text, "html5lib")

            # Address
            address_element = soup.find("td", attrs={"itemprop": "address"})
            if address_element and address_element.span:
                address = str(address_element.span.contents[0])
                address_details = await self._parse_address(address)
                results.update(address_details)

            # Registrant
            registrant_element = soup.find("tr", attrs={"itemprop": "alumni"})
            if registrant_element:
                registrant_element = registrant_element.find("span", attrs={"itemprop": "name"})
                if registrant_element and registrant_element.a:
                    results["registrant"] = registrant_element.a.contents[0]

            # Phone
            phone_element = soup.find("table", attrs={"class": "table-taxinfo"})
            if phone_element:
                phone_element = phone_element.find("td", attrs={"itemprop": "telephone"})
                if phone_element and phone_element.span:
                    phone = phone_element.span.contents[0]
                    results["phone"] = phone.replace(" ", "")

            # Business sectors
            career_element = soup.find("table", attrs={"class": "table"})
            if career_element:
                career_element = career_element.findAll("strong")
                if len(career_element) > 1 and career_element[1].a:
                    results["business_sectors"] = career_element[1].a.contents[0]

            return results
        except Exception as e:
            print("[Error] Get tax details: ", e)
            return results

    async def get_company_name(self, tax_code):
        url = f"https://api.vietqr.io/v2/business/{tax_code}"
        response_json = await self._http_get(url, return_json=True)
        if response_json.get("data"):
            return response_json["data"]["name"]

        url = f"https://tracuumst.com/tim-kiem?q={tax_code}"
        response_text = await self._http_get(url)
        soup = BeautifulSoup(response_text, "html5lib")
        try:
            name_element = soup.find("div", attrs={"class": "card-header"})
            if name_element:
                name_element = name_element.find("a", attrs={"class": "text-decoration-none"})
                return name_element.contents[0]
        except Exception as e:
            print("[Error] Get name company: ", e)
        return None

    async def get_address_vietqr(self, tax_code):
        url = f"https://api.vietqr.io/v2/business/{tax_code}"
        response_json = await self._http_get(url, return_json=True)
        if not response_json.get("data"):
            return {}
        address_vietqr = response_json["data"]["address"]
        return await self._parse_address(address_vietqr)

    async def get_tax(self, tax_code: str):
        results = {"tax_code": tax_code}
        try:
            company_name = await self.get_company_name(tax_code)
            if not company_name:
                results["status"] = "failed"
                return results
            results["name"] = company_name

            tax_details = await self.get_tax_details(results["name"], tax_code)
            if not tax_details:
                tax_details = await self.get_address_vietqr(tax_code)
            results.update(tax_details)
            results["status"] = "success"
            return results
        except Exception:
            traceback.print_exception(*sys.exc_info())
            results["status"] = "failed"
            return results


tax_services = TaxServices()
