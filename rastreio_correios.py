import requests
from lxml.html import fromstring

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.77 Safari/537.36 '
}
url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?'


def filter_local_label_tag(elem):
    label = elem.xpath('label')
    if label:
        return ' '.join(label[0].text.split())
    return elem.xpath('text()[3]')[0].strip()


def formata(lst):
    return {'DATA': lst[0].text,
            'HORA': lst[0].xpath('text()[2]')[0].strip(),
            'LOCAL': filter_local_label_tag(lst[0]),
            'SITUACAO': lst[1].xpath('strong')[0].text,
            'DESCRICAO': ' '.join(lst[1].xpath('text()')[2].split())}


def main(codigo):
    """Rastreio Correios

        Args:
            codigo (str): codigo de rastreio.
        Returns:
                (list): Uma lista de dicionarios contendo cada atualizacao nos dados.
    """
    res = requests.post(url, headers=header, data={'objetos': codigo}).content
    html = fromstring(res)
    tables = html.find_class('listEvent sro')
    return [formata(i.find('tr').findall('td')) for i in tables]


#  if __name__ == '__main__':
#      print(main('LB192989285HK'))
