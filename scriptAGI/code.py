#!/usr/bin/python

# importar bibliotecas

import sys
import re
import requests
import string

# CODIGO PROVENINETE DO LIVRO
# Read and ignore AGI environment (read until blank line)
env={}
while 1:
	line = sys.stdin.readline().strip()
	if line == '':
		break
	key,data = line.split(':')
	if key[:4] <> 'agi_':
		#skip input that doesn't begin with agi_
		sys.stderr.write("Did not work!\n");
		sys.stderr.flush()
		continue
	key = key.strip()
	data = data.strip()
	if key <> '':
		env[key] = data
	sys.stderr.write("AGI Environment Dump:\n");
	sys.stderr.flush()
	for key in env.keys():
		sys.stderr.write(" -- %s = %s\n" % (key, env[key]))
		sys.stderr.flush()

def checkresult (params):
	params = params.rstrip()
	if re.search('^200',params):
		result = re.search('result=(\d+)',params)
		if (not result):
			sys.stderr.write("FAIL ('%s')\n" % params)
			sys.stderr.flush()
			return -1
		else:
			result = result.group(1)
			#debug("Result:%s Params:%s" % (result, params))
			sys.stderr.write("PASS (%s)\n" % result)
			sys.stderr.flush()
			return result
	else:
		sys.stderr.write("FAIL (unexpected result '%s')\n" % params)
		sys.stderr.flush()
		return -2




url = "http://www.ctt.pt/feapl_2/app/open/postalCodeSearch/postalCodeSearch.jspx"

#recupera variaveis do Asterisk

code1= sys.argv[1]
code2= sys.argv[2]


payload = "?cp4="+code1+"&cp3="+code2+"&method%3AsearchPC2=Procurar"
link=url+payload

# send HTTP Post Request to url and with the code in the body
resp = requests.post(link)
resp_str=resp.text


#ENCONTRAR RESULTADO
vect = resp_str.split('<div class="highlighted-result text-left">')
result1 = vect[1].split('</div>',1)

result1 = result1[0].split('<h4 class="subheader">')

res1= result1[1].split('</h4>')
res1=res1[0]

result2= result1[2].split('</h4>')
res2=result2[0].replace(',', '.')


result3=result2[1].split('<h3 class="subheader">')
res3= result3[1].split('</h3>')
res4= res3[1].split('<h2>')
res4= res4[1].split('</h2>')
res3=res3[0]
res4= res4[0] 


sys.stdout.write("SET VARIABLE \"%s\" \"%s\"\n" % ("resp1",res1.encode('utf-8'))) 
sys.stdout.flush()
result = sys.stdin.readline().strip()
checkresult(result)
sys.stdout.write("SET VARIABLE \"%s\" \"%s\"\n" % ("resp2",res2.encode('utf-8')))
sys.stdout.flush()
result = sys.stdin.readline().strip()
checkresult(result)
sys.stdout.write("SET VARIABLE \"%s\" \"%s\"\n" % ("resp3",res3.encode('utf-8')))
sys.stdout.flush()
result = sys.stdin.readline().strip()
checkresult(result)
sys.stdout.write("SET VARIABLE \"%s\" \"%s\"\n" % ("resp4",res4.encode('utf-8')))
sys.stdout.flush()
result = sys.stdin.readline().strip()
checkresult(result)


