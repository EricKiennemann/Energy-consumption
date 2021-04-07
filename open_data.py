"""
https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-iris&q=&rows=10000&facet=operateur&facet=annee&facet=filiere&facet=libelle_commune&facet=code_departement&facet=libelle_region&refine.code_departement=75&refine.annee=2019
"""

from constants import OPEN_DATA_TIMEOUT, OPEN_DATA_RETRIES
import requests
import os
from collections import defaultdict

class IrisConsumption(object):

    def __init__(self, dept, year, dataset = 'conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-iris', server = 'https://opendata.agenceore.fr/api' ):
        """initialise the Open_data class

        Parameters
        ----------
        dept : int
            department number
        year : int
            year for the data
        """

        self.dept = dept
        self.year = year
        self.dataset = dataset

        self.server = server
        if not self.server:
            raise ValueError("No osrm server given")

        self.timeout = OPEN_DATA_TIMEOUT

        # Session definition
        self.session = requests.Session()
        self.session.mount(
            "https://",
            requests.adapters.HTTPAdapter(
                max_retries=OPEN_DATA_RETRIES
            ),
        )

    def _build_base_request(self):

        #base_request = "records/1.0/search/?dataset={}&q=&rows=10000&facet=operateur&facet=annee&facet=filiere&facet=libelle_commune&facet=code_departement&facet=libelle_region&refine.code_departement={}&refine.annee={}".format(
        base_request = "records/1.0/search/?dataset={}&q=&rows=10000&facet=annee&facet=libelle_commune&facet=code_departement&facet=libelle_region&refine.code_departement={}&refine.annee={}".format(
                        self.dataset, self.dept,self.year
        )

        return os.path.join(self.server, base_request)

    def _get_result(self):

        request_url = self._build_base_request()

        try:
            response = self.session.get(request_url, timeout=self.timeout)

            if response.status_code != requests.codes.ok:
                print(f"error in requestiong data : {response.text}")
                return None

            result = response.json()
            return result


        except (IndexError, ValueError):
            return None

    def _get_records(self):

        return self._get_result()['records']

    def get_fields(self):

        records = self._get_records()

        return [record['fields'] for record in records]

    def consumption_by_iris(self):

        fields = self.get_fields()
        consumption=defaultdict(int)
        for field in fields:
            consumption[field['code_iris']] += field['consor']
        return consumption

if __name__ == '__main__':


    energy = IrisConsumption(75,2019)
    print(energy.consumption_by_iris())
