"""
Sample log file parser which will parse the log file, get the IP addressed with their count frequency and export the data to a csv file
"""

import re
import csv
import collections
import json
from typing import List
import sys,getopt
import difflib
from match_complete import *

class Item(object):
    def __init__(self, childItemRel):
        super().__init__()
        self.childItemRel=childItemRel

class RelationOb(object):
    def __init__(self, childrelName:Item ,childrel:List [Item]):
        super().__init__()
        self.childrelName= childrelName
        self.childrel=childrel

    def addRelItem(self,itenIns:Item):
        self.childrel.append(itenIns)

class Parser(object):

    def __init__(self,argv):
        super().__init__()
        self.filename=''
        self.traceID=''
        self.outFile =''

        try:
            opts, args = getopt.getopt(argv,"hi:t:o:",["ifile=","itrace=","ofile="])
        except getopt.GetoptError:
            print ('logAnalyze.py -i <inputfile>  -t <inputTrace> -o <outputfile>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print ('logAnalyze.py -i <inputfile>  -t <inputTrace> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                self.inFile = arg
            elif opt in ("-t", "--itrace"):
                self.traceID = arg
            elif opt in ("-o", "--ofile"):
                self.outFile = arg
        print ('Input file is ', self.inFile)
        print ('Input trace is ', self.traceID)
        print ('Output file is ', self.outFile)
        
    def log_file_reader(self):
        filename =self.inFile
        traceID = self.traceID

        with open(filename) as f:
            log = f.read()
            #regex= "Flow - CustomerHandling Orchestration. Beginning of step CO.*?"+traceID+"|Flow - Product Order Orchestration. Beginning of step PO.*?"+traceID+"|Request for .*?uams_d1_get_token.fxml|CDM output.*?</com:CDM>"
            regex= "Flow - CustomerHandling Orchestration. Beginning of step CO.*?"+traceID+"|Flow - Product Order Orchestration. Beginning of step PO.*?"+traceID+"|CDM output.*?"+traceID+".*?</com:CDM>|Request for .*?call is"
            #regex= "Flow - Product Order Orchestration. Beginning of step PO.*?"+traceID
            print(regex)
            
            ip_list = re.findall(regex, log,re.DOTALL)

            metind=0
            while  metind < len(ip_list):
                itemInst= ip_list[metind]
                if itemInst.startswith('Flow - Product Order Orchestration. Beginning of step P'):
                    print (itemInst)
                metind= metind+1

            items_arr=[]
            cdm_arr=''
            cdm_comp_arr=[]
            metind=0
            while  metind < len(ip_list):
                itemInst= ip_list[metind]
                metind=metind+1
                itemInst= itemInst.replace('\n','')
        
                item= Item(itemInst)
                if itemInst.startswith('Flow - Product Order Orchestration. Beginning of') or itemInst.startswith('Flow - CustomerHandling Orchestration. Beginning of step CO'):
                    relationOb =RelationOb(item,[])
                    while  metind < len(ip_list):
                        itemInst= ip_list[metind]
                        itemInst= itemInst.replace('\n','')
                        itemInst= itemInst.replace('\\','')
                        metind=metind+1
                        if itemInst.startswith('Request for'):
                            item= Item(itemInst)
                            relationOb.addRelItem(item)
                        elif  itemInst.startswith('CDM output'):
                            item= Item(itemInst)
                            if cdm_arr !='':
                                cdm_comp_arr= show_comparison(cdm_arr, itemInst, sidebyside=False)
                                relationOb.addRelItem(Item('Existing Step CDM:'+cdm_comp_arr[0]))
                                relationOb.addRelItem(Item('Prev     Step CDM:'+cdm_comp_arr[1]))
                            cdm_arr= itemInst
                        else:
                            break
                    items_arr.append(relationOb)
            return items_arr
        

    def write_to_json(self,data):
        outFile= self.outFile
        with open(outFile,'w') as jsonFile:
            jsonFile.write(json.dumps(data, default=lambda o: o.__dict__, indent=4))


if __name__ == "__main__":
    result=[]
    parser= Parser(sys.argv[1:])
    #parser= Parser('TOPIC-amil-wf-service-f68d47d49-ntqm9-TOPIC-amil-wf-service.log','PROJ_b1ea1edb-498e-4ba2-801f-4082bd2f433e','PROJ_b1ea1edb-498e-4ba2-801f-4082bd2f433e.json')
    datalog=parser.log_file_reader()
    parser.write_to_json(datalog)
    # s1 = "CDM output: <com:CDM xmlns:com=\"http://amdocs/hub/CommonDataModel_V330\">\n  <Info>\n    <CallingSystem>MoD</CallingSystem>\n    <WFProcessName/>\n    <ReceiveDate>2023-05-10T14:19:46</ReceiveDate>\n    <CDMTxID>PROJ_9345cbd4-0fef-44e4-9a94-a1166076ab77</CDMTxID>\n    <CDMEntityType>O</CDMEntityType>\n    <GeneralTxID/>\n  </Info>\n  <Order>\n    <OrderID>PROJ_9345cbd4-0fef-44e4-9a94-a1166076ab77</OrderID>\n    <S_OrderID>PROJ_9345cbd4-0fef-44e4-9a94-a1166076ab77</S_OrderID>\n    <OrderStatus>P</OrderStatus>\n    <Attributes>\n      <Attribute>\n        <Code>externalOrder</Code>\n        <Value>{\"type\":\"OSF\",\"id\":\"5781155576\"}</Value>\n      </Attribute>\n    </Attributes>\n    <TargetOrder>\n      <Dependency>productOrder_null_0cd14b63-1fd9-45aa-973a-6490a3455727</Dependency>\n      <Name>COMPOSITE_ORDER</Name>\n      <T_OrderID/>\n      <T_CustomerID/>\n      <Attributes>\n        <Attribute>\n          <Code>description</Code>\n          <Value>Customer Regrets Replace Offer</Value>\n        </Attribute>\n        <Attribute>\n          <Code>orderDate</Code>\n          <Value>2023-05-10T14:19:36.790Z</Value>\n        </Attribute>\n        <Attribute>\n          <Code>productOrderRelatedParty</Code>\n          <Value>[{\"role\":\"customer\",\"type\":\"Customer\",\"id\":\"101000000796\"}]</Value>\n        </Attribute>\n        <Attribute>\n          <Code>billingAccountId</Code>\n          <Value>20300000000820</Value>\n        </Attribute>\n        <Attribute>\n          <Code>productOrderChannel</Code>\n          <Value>[{\"id\":\"CallCenter\",\"name\":\"CallCenter\"}]</Value>\n        </Attribute>\n        <Attribute>\n          <Code>productOrderExternalIdentifier</Code>\n          <Value>[{\"type\":\"OriginalProductOrderID\",\"id\":\"\"}]</Value>\n        </Attribute>\n        <Attribute>\n          <Code>modifyReason</Code>\n          <Value>[{\"name\":\"Kundenanfrage\",\"reasonText\":\"Kundenanfrage\"}]</Value>\n        </Attribute>\n      </Attributes>\n      <Product>\n        <T_ProductPath/>\n        <ProductID>1291</ProductID>\n        <ParentProductID/>\n        <T_ProductID>400000000000001119</T_ProductID>\n        <Status>Draft</Status>\n        <SentToTargetDate>2023-05-10T14:19:46.633+0000</SentToTargetDate>\n        <Product>\n          <T_ProductUniqueCode>CompositeOrder</T_ProductUniqueCode>\n          <T_ProductPath>/null</T_ProductPath>\n          <ProductID>1292</ProductID>\n          <ParentProductID/>\n          <T_ProductID/>\n          <Status>N</Status>\n          <SentToTargetDate>2023-05-10T14:19:46.639+0000</SentToTargetDate>\n          <Attributes>\n            <ActivityType>terminate</ActivityType>\n            <OfferCode>Red Internet 120 Cable</OfferCode>\n            <ActionCode>Internet_Only_Offer</ActionCode>\n            <OfferID>f0229a03-36b9-4aac-b466-1d4a62fef019</OfferID>\n            <ProductLevel>701000000000002093</ProductLevel>\n            <Attribute>\n              <Code>orderItemReferenceId</Code>\n              <Value>refRedInternet120Cable</Value>\n            </Attribute>\n          </Attributes>\n        </Product>\n        <Product>\n          <T_ProductUniqueCode>CompositeOrder</T_ProductUniqueCode>\n          <T_ProductPath>/null</T_ProductPath>\n          <ProductID>1293</ProductID>\n          <ParentProductID/>\n          <T_ProductID>400000000000001119_410000000000005127</T_ProductID>\n          <Status>Draft</Status>\n          <SentToTargetDate>2023-05-10T14:19:46.643+0000</SentToTargetDate>\n          <Attributes>\n            <ActivityType>terminate</ActivityType>\n            <OfferCode>Access</OfferCode>\n            <ActionCode>MLP_Access</ActionCode>\n            <OfferID>41230743-b2c7-4bad-a4b9-de1727e26c72</OfferID>\n            <RelatedProductID>c5a99a33-2b07-441e-8fb8-ffe6c1710342</RelatedProductID>\n            <ProductLevel>701000000000002096</ProductLevel>\n            <Attribute>\n              <Code>orderItemReferenceId</Code>\n              <Value>refAccess</Value>\n            </Attribute>\n            <Attribute>\n              <Code>D1modifyReason</Code>\n              <Value>[{\"name\":\"Kundenanfrage\",\"reasonText\":\"Kundenanfrage\",\"action\":\"terminate\"}]</Value>\n            </Attribute>\n            <Attribute>\n              <Code>Legal_Entity_ID</Code>\n              <Value>DE37</Value>\n              <AdditionalValue>D1characteristic</AdditionalValue>\n            </Attribute>\n            <Attribute>\n              <Code>Network_Technology</Code>\n              <Value>Cable</Value>\n              <AdditionalValue>D1characteristic</AdditionalValue>\n            </Attribute>\n            <Attribute>\n              <Code>TOPIC_Network_Indicator</Code>\n              <Value>true</Value>\n              <AdditionalValue>D1characteristic</AdditionalValue>\n            </Attribute>\n          </Attributes>\n        </Product>\n      </Product>\n    </TargetOrder>\n  </Order>\n  <Customer>\n    <CustomerStatus>P</CustomerStatus>\n    <Address>\n      <Attributes>\n        <Attribute>\n          <Code>geoAddressAction</Code>\n          <Value>keep</Value>\n        </Attribute>\n      </Attributes>\n    </Address>\n    <Customer>\n      <Individual>\n        <Attributes>\n          <Attribute>\n            <Code>action</Code>\n            <Value>keep</Value>\n          </Attribute>\n        </Attributes>\n      </Individual>\n    </Customer>\n  </Customer>\n</com:CDM>"
    # s2 = "CDM output: <com:CDM xmlns:com=\"http://amdocs/hub/CommonDataModel_V330\">\n  <Info>\n    <CallingSystem>MoD</CallingSystem>\n    <WFProcessName/>\n    <ReceiveDate>2023-05-10T14:19:46</ReceiveDate>\n    <CDMTxID>PROJ_9345cbd4-0fef-44e4-9a94-a1166076ab77</CDMTxID>\n    <CDMEntityType>O</CDMEntityType>\n    <GeneralTxID/>\n  </Info>\n  <Order>\n    <OrderID>PROJ_9345cbd4-0fef-44e4-9a94-a1166076ab77</OrderID>\n    <S_OrderID>PROJ_9345cbd4-0fef-44e4-9a94-a1166076ab78</S_OrderID>\n    <OrderStatus>P</OrderStatus>\n    <Attributes>\n      <Attribute>\n        <Code>externalOrder</Code>\n        <Value>{\"type\":\"OSF\",\"id\":\"5781155576\"}</Value>\n      </Attribute>\n    </Attributes>\n    <TargetOrder>\n      <Dependency>productOrder_null_0cd14b63-1fd9-45aa-973a-6490a3455727</Dependency>\n      <Name>COMPOSITE_ORDER</Name>\n      <T_OrderID/>\n      <T_CustomerID/>\n      <Attributes>\n        <Attribute>\n          <Code>description</Code>\n          <Value>Customer Regrets Replace Offer</Value>\n        </Attribute>\n        <Attribute>\n          <Code>orderDate</Code>\n          <Value>2023-05-10T14:19:36.790Z</Value>\n        </Attribute>\n        <Attribute>\n          <Code>productOrderRelatedParty</Code>\n          <Value>[{\"role\":\"customer\",\"type\":\"Customer\",\"id\":\"101000000796\"}]</Value>\n        </Attribute>\n        <Attribute>\n          <Code>billingAccountId</Code>\n          <Value>20300000000820</Value>\n        </Attribute>\n        <Attribute>\n          <Code>productOrderChannel</Code>\n          <Value>[{\"id\":\"CallCenter\",\"name\":\"CallCenter\"}]</Value>\n        </Attribute>\n        <Attribute>\n          <Code>productOrderExternalIdentifier</Code>\n          <Value>[{\"type\":\"OriginalProductOrderID\",\"id\":\"400000000000001118\"}]</Value>\n        </Attribute>\n        <Attribute>\n          <Code>modifyReason</Code>\n          <Value>[{\"name\":\"Kundenanfrage\",\"reasonText\":\"Kundenanfragr\"}]</Value>\n        </Attribute>\n      </Attributes>\n      <Product>\n        <T_ProductPath/>\n        <ProductID>1291</ProductID>\n        <ParentProductID/>\n        <T_ProductID>400000000000001119</T_ProductID>\n        <Status>Draft</Status>\n        <SentToTargetDate>2023-05-10T14:19:46.633+0000</SentToTargetDate>\n        <Product>\n          <T_ProductUniqueCode>CompositeOrder</T_ProductUniqueCode>\n          <T_ProductPath>/null</T_ProductPath>\n          <ProductID>1292</ProductID>\n          <ParentProductID/>\n          <T_ProductID/>\n          <Status>N</Status>\n          <SentToTargetDate>2023-05-10T14:19:46.639+0000</SentToTargetDate>\n          <Attributes>\n            <ActivityType>terminate</ActivityType>\n            <OfferCode>Red Internet 120 Cable</OfferCode>\n            <ActionCode>Internet_Only_Offer</ActionCode>\n            <OfferID>f0229a03-36b9-4aac-b466-1d4a62fef019</OfferID>\n            <ProductLevel>701000000000002093</ProductLevel>\n            <Attribute>\n              <Code>orderItemReferenceId</Code>\n              <Value>refRedInternet120Cable</Value>\n            </Attribute>\n          </Attributes>\n        </Product>\n        <Product>\n          <T_ProductUniqueCode>CompositeOrder</T_ProductUniqueCode>\n          <T_ProductPath>/null</T_ProductPath>\n          <ProductID>1293</ProductID>\n          <ParentProductID/>\n          <T_ProductID>400000000000001119_410000000000005127</T_ProductID>\n          <Status>Draft</Status>\n          <SentToTargetDate>2023-05-10T14:19:46.643+0000</SentToTargetDate>\n          <Attributes>\n            <ActivityType>terminate</ActivityType>\n            <OfferCode>Access</OfferCode>\n            <ActionCode>MLP_Access</ActionCode>\n            <OfferID>41230743-b2c7-4bad-a4b9-de1727e26c72</OfferID>\n            <RelatedProductID>c5a99a33-2b07-441e-8fb8-ffe6c1710342</RelatedProductID>\n            <ProductLevel>701000000000002096</ProductLevel>\n            <Attribute>\n              <Code>orderItemReferenceId</Code>\n              <Value>refAccess</Value>\n            </Attribute>\n            <Attribute>\n              <Code>D1modifyReason</Code>\n              <Value>[{\"name\":\"Kundenanfrage\",\"reasonText\":\"Kundenanfrage\",\"action\":\"terminate\"}]</Value>\n            </Attribute>\n            <Attribute>\n              <Code>Legal_Entity_ID</Code>\n              <Value>DE37</Value>\n              <AdditionalValue>D1characteristic</AdditionalValue>\n            </Attribute>\n            <Attribute>\n              <Code>Network_Technology</Code>\n              <Value>Cable</Value>\n              <AdditionalValue>D1characteristic</AdditionalValue>\n            </Attribute>\n            <Attribute>\n              <Code>TOPIC_Network_Indicator</Code>\n              <Value>true</Value>\n              <AdditionalValue>D1characteristic</AdditionalValue>\n            </Attribute>\n          </Attributes>\n        </Product>\n      </Product>\n    </TargetOrder>\n  </Order>\n  <Customer>\n    <CustomerStatus>P</CustomerStatus>\n    <Address>\n      <Attributes>\n        <Attribute>\n          <Code>geoAddressAction</Code>\n          <Value>keep</Value>\n        </Attribute>\n      </Attributes>\n    </Address>\n    <Customer>\n      <Individual>\n        <Attributes>\n          <Attribute>\n            <Code>action</Code>\n            <Value>keep</Value>\n          </Attribute>\n        </Attributes>\n      </Individual>\n    </Customer>\n  </Customer>\n</com:CDM>"
    # print('Above-below comparison')
    # print('-------------------------------------------------------------------------------------')
    # result =show_comparison(s1, s2, sidebyside=False)
    # print('---------------------------------------------S1----------------------------------------')
    # print(result[0])
    # print('---------------------------------------------S2----------------------------------------')
    # print(result[1])

    #matcher = difflib.SequenceMatcher(a=s1, b=s2)
    #print("Matching Sequences:")
    #for match in matcher.get_matching_blocks():
    #    print("Match             : {}".format(match))
    #    print("Matching Sequence : {}".format(s1[match.a:match.a+match.size]))
        #https://towardsdatascience.com/side-by-side-comparison-of-strings-in-python-b9491ac858


#print ('logAnalyze.py -i <inputfile>  -t <inputTrace> -o <outputfile>')

#python logAnalyz.py -i TOPIC-amil-wf-service-f68d47d49-ntqm9-TOPIC-amil-wf-service.log  -t PROJ_b1ea1edb-498e-4ba2-801f-4082bd2f433e -o PROJ_b1ea1edb-498e-4ba2-801f-4082bd2f433e.json
