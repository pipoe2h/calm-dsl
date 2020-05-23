artifactory_new_password = '@@{ARTIFACTORY_PASSWORD}@@'

# Authenticate and store cookies
api_url = 'http://@@{address}@@:8082/ui/api/v1/ui/auth/login?_spring_security_remember_me=false'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}

payload = {"user":"admin","password":"password","type":"login"}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    cookies = r.cookies.get_dict()
    accesstoken = cookies['ACCESSTOKEN']
    refreshtoken = cookies['REFRESHTOKEN']

else:
    print("Post request failed", r.content)
    exit(1)

# Change default password    
api_url = 'http://@@{address}@@:8082/ui/api/v1/ui/onboarding/changePassword'
cookies = {'ACCESSTOKEN': accesstoken, 'REFRESHTOKEN': refreshtoken}
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}

payload = {"userName":"admin","oldPassword":"password","newPassword1":artifactory_new_password,"newPassword2":artifactory_new_password}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, cookies=cookies, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)

else:
    print("Post request failed", r.content)
    exit(1)

# Delete default local repo
api_url = 'http://@@{address}@@:8082/ui/api/v1/ui/admin/repositories/example-repo-local/delete?type=local'

r = urlreq(api_url, verb='DELETE', headers=headers, cookies=cookies, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)

else:
    print("Post request failed", r.content)
    exit(1)

# Allow anonymous access
api_url = 'http://@@{address}@@:8082/ui/api/v1/ui/securityconfig'

r = urlreq(api_url, verb='GET', headers=headers, cookies=cookies, verify=False)
if r.ok:
    resp = json.loads(r.content)

    resp['anonAccessEnabled'] = True

    r = urlreq(api_url, verb='PUT', params=json.dumps(resp), headers=headers, cookies=cookies, verify=False)
    if r.ok:
        resp = json.loads(r.content)
        print(resp)

    else:
        print("Post request failed", r.content)
        exit(1)
else:
    print("Post request failed", r.content)
    exit(1)

# Set filesize max to 5GB
api_url = 'http://@@{address}@@:8082/ui/api/v1/ui/generalConfig'

r = urlreq(api_url, verb='GET', headers=headers, cookies=cookies, verify=False)
if r.ok:
    resp = json.loads(r.content)

    resp['fileUploadMaxSize'] = 5000

    r = urlreq(api_url, verb='PUT', params=json.dumps(resp), headers=headers, cookies=cookies, verify=False)
    if r.ok:
        resp = json.loads(r.content)
        print(resp)

    else:
        print("Post request failed", r.content)
        exit(1)

else:
    print("Post request failed", r.content)
    exit(1)

# Create Official ISOs repo
api_url = 'http://@@{address}@@:8082/ui/api/v1/ui/admin/repositories'

payload = {
    "type": "localRepoConfig",
    "typeSpecific": {
        "localChecksumPolicy": "CLIENT",
        "repoType": "Generic",
        "icon": "generic",
        "text": "Generic",
        "listRemoteFolderItems": True,
        "url": ""
    },
    "advanced": {
        "cache": {
            "keepUnusedArtifactsHours": "",
            "retrievalCachePeriodSecs": 7200,
            "assumedOfflineLimitSecs": 300,
            "missedRetrievalCachePeriodSecs": 1800
        },
        "network": {
            "socketTimeout": 15000,
            "syncProperties": False,
            "lenientHostAuth": False,
            "cookieManagement": False
        },
        "blackedOut": False,
        "allowContentBrowsing": False
    },
    "basic": {
        "includesPattern": "**/*",
        "includesPatternArray": [
            "**/*"
        ],
        "excludesPatternArray": [],
        "layout": "simple-default"
    },
    "general": {
        "repoKey": "official-isos"
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, cookies=cookies, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)

else:
    print("Post request failed", r.content)
    exit(1)

# Create Calm ISOs repo
payload['general']['repoKey'] = "calm-isos"

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, cookies=cookies, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)

else:
    print("Post request failed", r.content)
    exit(1)

# Create AutoYast Profiles repo
payload['general']['repoKey'] = "autoyast-profiles"

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, cookies=cookies, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)

else:
    print("Post request failed", r.content)
    exit(1)