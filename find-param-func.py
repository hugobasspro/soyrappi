from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcodeartspipeline.v2.region.codeartspipeline_region import CodeArtsPipelineRegion
from huaweicloudsdkcodeartspipeline.v2 import *
import sys
import json

def main(app_type, postfix, service):
    try:
        doc=  {
        'app-type': 'frontend',
        'postfix': 'co',
        'service': 'soyrappi',
        'cert-name': 'scm-355c25',
        'region': 'la-north-2',
        'bucket': 'soyrappi',
        'domain-web': 'davidcm.org',
        'bucket-folder': 'co',
        'project-id': '8357e2c517ac472889085a0af0a87f37',
        'pipeline-id': '0cd6ff1d77fc478896df83511d2ecc1e',
        'compiler': 'npm',
        'version': '10',
        'build-script': 'run build-develop',
        'build-folder': 'build',
        'repository': 'git@bitbucket.org:rappinc/soyrappi.git',
        'branch': 'master',
        'cors': 'false'
        }
        return doc
    except Exception as e:
        print(f"Exception occurred while querying mongo's param collection: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python find-param.py <app_type> <postfix> <service> <access_key_id> <secret_access_key> <region> <subdomain>")
        sys.exit(1)

    app_type, postfix, service, ak, sk, region, subdomain = sys.argv[1:]

    credentials = BasicCredentials(ak, sk)
    client_cab = CodeArtsPipelineClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(CodeArtsPipelineRegion.value_of(region)) \
        .build()

    result = main(app_type, postfix, service)
    if result == None:
        print(f"No record exists for the combination app_type: {app_type}, postfix: {postfix}, service: {service}")
        sys.exit(1)
    else:
        print(result)

    try:
        request = RunPipelineRequest()
        request.project_id = result['project-id']
        request.pipeline_id = result['pipeline-id'] # Number when editing the pipeline
        listVariablesbody = [
            RunPipelineDTOVariables(
                name="domainName",
                value=subdomain+"."+result['domain-web']
            ),
            RunPipelineDTOVariables(
                name="bucketFolder",
                value=result['bucket-folder']
            ),
            RunPipelineDTOVariables(
                name="sslCertificateName",
                value=result['cert-name']
            ),
            RunPipelineDTOVariables(
                name="region",
                value=result['region']
            ),
            RunPipelineDTOVariables(
                name="ak",
                value=ak
            ),
            RunPipelineDTOVariables(
                name="sk",
                value=sk
            ),
            RunPipelineDTOVariables(
                name="bucketName",
                value=result['bucket']
            ),
            RunPipelineDTOVariables(
                name="compiler",
                value=result['compiler']
            ),
            RunPipelineDTOVariables(
                name="version",
                value=result["version"]
            ),
            RunPipelineDTOVariables(
                name="repository",
                value=result['repository']
            ),
            RunPipelineDTOVariables(
                name="branch",
                value=result['branch']
            ),
            RunPipelineDTOVariables(
                name="buildScript",
                value=result['build-script']
            ),
            RunPipelineDTOVariables(
                name="buildFolder",
                value=result['build-folder']
            ),
            RunPipelineDTOVariables(
                name="cors",
                value=result['cors']
            )
        ]
        request.body = RunPipelineDTO(
            variables=listVariablesbody
        )
        response = client_cab.run_pipeline(request)
        print(response)
        sys.exit(0)
    except Exception as e:
        print(f"Exception occurred while creating pipeline '{result['pipeline-id']}': {e}")
        sys.exit(1)