import subprocess
import random

def create_api_client(swagger_guid):
    package_identifier = random.randint(100000, 999999)
    swagger_schema_file = 'swagger_{0}.json'.format(swagger_guid)
    run_cmd = './powershell-script/CreateNgApiClientNpmPackage.sh' 
    subprocess.check_call([run_cmd, swagger_schema_file, str(package_identifier)])
    return package_identifier

def publish_package(package_identifier):
    package_path = 'api-client-{0}'.format(package_identifier)
    run_cmd = './powershell-script/PublishApiClientPackage.sh'
    subprocess.check_call([run_cmd, package_path])
