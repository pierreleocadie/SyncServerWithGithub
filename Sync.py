import os, json

PERSONAL_ACCESS_TOKEN = "YOUR_PERSONAL_GITHUB_ACCESS_TOKEN"
OWNER = "GITHUB_REPO_OWNER"
REPO = "GITHUB_REPO_NAME"
CONTAINER = "DOCKER_CONTAINER_NAME"
PATH = "PATH_TO_REPO"
PORT_MAPPING = "PORT_MAPPING_FOR_DOCKER_CONTAINER"

CURL_REQUEST = f'curl --request GET \
    --url "https://api.github.com/repos/{OWNER}/{REPO}/commits" \
    --header "Accept: application/vnd.github+json" \
    --header "Authorization: Bearer {PERSONAL_ACCESS_TOKEN}" > {PATH}/lastCommit-1.json'

BUILD_AND_RUN_CONTAINER = f"cd {PATH}/; \
			git clone https://github.com/{OWNER}/{REPO}.git; \
                        docker stop {CONTAINER}; \
                        docker rm {CONTAINER}; \
                        cd {PATH}/{REPO}; \
                        docker build -t {CONTAINER} .; \
                        docker run -d --name {CONTAINER} -p {PORT_MAPPING} {CONTAINER}"

def checkRemoveBuildRun():
    if(os.path.exists(f"{PATH}/{REPO}")):
        os.system(f"rm -rf {PATH}/{REPO}")
    os.system(BUILD_AND_RUN_CONTAINER)

if(os.path.exists(f"{PATH}/lastCommit.json")):
    os.system(CURL_REQUEST)
    with open(f"{PATH}/lastCommit.json", "r") as f:
        if(f.read() != open(f"{PATH}/lastCommit-1.json", "r").read()):
            print("New commit")
            checkRemoveBuildRun()
        os.system(f"rm {PATH}/lastCommit.json; \
        mv {PATH}/lastCommit-1.json {PATH}/lastCommit.json")
else:
    os.system(CURL_REQUEST)
    checkRemoveBuildRun()