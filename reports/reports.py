from urllib import parse
from django.conf import settings
from django.http import HttpResponse


class BaseJasperReport(object):
    report_name = ''
    filename = ''

    def __init__(self, request, params):
        self.request = request
        self.params = params
        self.auth = (settings.JASPER_USER, settings.JASPER_PASSWORD)
        super(BaseJasperReport, self).__init__()

    def get_url(self):
        url = r'{url}/flow.html?' \
              r'_flowId={flow_id}&' \
              r'ParentFolderUri={parent_folder_uri}&' \
              r'standAlone={stand_alone}&' \
              r'j_username={j_username}&' \
              r'j_password={j_password}&' \
              r'{param}'.format(
                url=self.get_domain(),
                flow_id='viewReportFlow',
                parent_folder_uri=r'/reports/arrimo_reports',
                stand_alone='true',
                j_username=settings.JASPER_USER,
                j_password=settings.JASPER_PASSWORD,
                param=parse.urlencode(self.params))
        return url

    def get_domain(self):
        import socket
        domain = socket.gethostbyname(socket.gethostname())
        return "http://{domain}:{port}/jasperserver".format(domain=settings.JASPER_DOMAIN, port=settings.JASPER_PORT)

    def get_report(self):
        req = requests.get(self.get_url(), params={}, auth=self.auth)
        return req.content

    def render_to_response(self):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(self.filename)
        response.write(self.get_report())
        return response


