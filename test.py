#!/usr/bin/env python
import web
import json
import simplejson

web.config.debug = False

urls = (
    '/(.*)', 'handleRequest',
)

SUPER = 25
LARGE = 10
MEDIUM = 5
SMALL = 1
REQUEST_SIZES = [SUPER, LARGE, MEDIUM, SMALL]

SUPER_IP_1 = "10.0.7."
SUPER_IP_2 = "10.0.8."
LARGE_IP_1 = "10.0.5."
LARGE_IP_2 = "10.0.6."
MEDIUM_IP_1 = "10.0.3."
MEDIUM_IP_2 = "10.0.4."
SMALL_IP_1 = "10.0.1."
SMALL_IP_2 = "10.0.2."


app = web.application(urls, globals())

class handleRequest:
    def assignRequestDistribution(self, num_recipients):
        if(num_recipients == 0):
            return []
        for request in REQUEST_SIZES:
            if request <= num_recipients:
                return [request] + self.assignRequestDistribution(num_recipients - request)

    def assignRoutes(self, requestDistribution, recipients):
        routes = [] 
        num_super = 0;
        num_large = 0;
        num_medium = 0;
        num_small = 0;
        recipient_index = 0;

        for request in requestDistribution:
            if request == SUPER:
                num_super += 1
                ip_address = None
                if num_super < 999:
                    ip_address = SUPER_IP_1 + str(num_super)
                else:
                    ip_address = SUPER_IP_2 + str(num_super - 999)
                recipient_arr = [];
                for i in range(0, SUPER):
                    recipient_arr.append(recipients[recipient_index])
                    recipient_index += 1
                tempDict = {}
                tempDict["ip"] = ip_address
                tempDict["recipients"] = recipient_arr
                routes.append(tempDict)

            elif request == LARGE:
                num_large += 1
                ip_address = None
                if num_large < 999:
                    ip_address = LARGE_IP_1 + str(num_large)
                else:
                    ip_address = LARGE_IP_2 + str(num_large - 999)
                recipient_arr = [];
                for i in range(0, LARGE):
                    recipient_arr.append(recipients[recipient_index])
                    recipient_index += 1
                tempDict = {}
                tempDict["ip"] = ip_address
                tempDict["recipients"] = recipient_arr
                routes.append(tempDict)

            elif request == MEDIUM:
                num_medium += 1
                ip_address = None
                if num_medium < 999:
                    ip_address = MEDIUM_IP_1 + str(num_medium)
                else:
                    ip_address = MEDIUM_IP_2 + str(num_medium - 999)
                recipient_arr = [];
                for i in range(0, MEDIUM):
                    recipient_arr.append(recipients[recipient_index])
                    recipient_index += 1
                tempDict = {}
                tempDict["ip"] = ip_address
                tempDict["recipients"] = recipient_arr
                routes.append(tempDict)

            elif request == SMALL:
                num_small += 1
                ip_address = None
                if num_small < 999:
                    ip_address = SMALL_IP_1 + str(num_small)
                else:
                    ip_address = SMALL_IP_2 + str(num_small - 999)
                recipient_arr = [];
                for i in range(0, SMALL):
                    recipient_arr.append(recipients[recipient_index])
                    recipient_index += 1
                tempDict = {}
                tempDict["ip"] = ip_address
                tempDict["recipients"] = recipient_arr
                routes.append(tempDict)

        return routes                    

    def POST(self, method_id):
        i = web.input()
        data = web.data() # you can get data use this method
        try:
            jsondata = simplejson.loads(data)
        except JSONDecodeError:
            abort(500)
        num_recipients = len(jsondata["recipients"])
        request_distribution = self.assignRequestDistribution(num_recipients)
       
        result = []
        routes = {}
        message = {}
        message["message"] = jsondata["message"]
        routes["routes"] = self.assignRoutes(request_distribution, jsondata["recipients"])
        result.append(message)
        result.append(routes)
        return json.dumps(result)

if __name__ == "__main__":
    app.run()
