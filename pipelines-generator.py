
from pathlib import Path
import os
import jinja2 as j2

TEMPLATE_FILE = 'bitbucket-pipelines.yml.j2'

DOCKERFILE_VERSION_ARG='JIRA_VERSION'

CORE_REPOS = ['atlassian/jira-core']
SOFTWARE_REPOS = ['atlassian/jira-software']
SD_REPOS = ['atlassian/jira-servicemanagement', 'atlassian/jira-servicedesk']

images = {
    'Jira Software': {
        11: {
            'mac_key': 'jira-software',
            'artefact': 'atlassian-jira-software',
            'start_version': '8.13',
            'default_release': True,
            'tag_suffixes': ['jdk11', 'ubuntu-jdk11'],
            'base_image': 'eclipse-temurin:11',
            'docker_repos': SOFTWARE_REPOS,
        }
    },
    'Jira Service Management': {
        11: {
            'mac_key': 'jira-servicedesk',
            'artefact': 'atlassian-servicedesk',
            'start_version': '4.13',
            'default_release': True,
            'tag_suffixes': ['jdk11', 'ubuntu-jdk11'],
            'base_image': 'eclipse-temurin:11',
            'docker_repos': SD_REPOS,
        }
    },
    'Jira Core': {
        11: {
            'mac_key': 'jira',
            'artefact': 'atlassian-jira-core',
            'start_version': '8.13',
            'default_release': True,
            'tag_suffixes': ['jdk11', 'ubuntu-jdk11'],
            'base_image': 'eclipse-temurin:11',
            'docker_repos': CORE_REPOS,
        }
    }
}


def main():
    jenv = j2.Environment(
        loader=j2.FileSystemLoader('.'),
        lstrip_blocks=True,
        trim_blocks=True)
    template = jenv.get_template(TEMPLATE_FILE)
    generated_output = template.render(images=images, batches=12)

    print(generated_output)

if __name__ == '__main__':
    main()
