# В нашей целевой модели обработки уязвимостей не используются платформы для компонентного анализа (например, dependency track),
# т.к. нет возможности автоматизированно и гарантированно устанавливать версии зависимостей и их типы из-за отсутсвия пакетного менеджера.
# Следовательно в нашем случае генерация SBOM в распространенных форматах не имеет смысла
# Данный файл - наработка на случай появления проектов, в которых будет возможность использовать платформы для компонентного анализа

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output import get_instance, OutputFormat

data = [
    {
        "directory": "./project_name\\bluez-5.15",
        "match": {
            "score": 0.9829545454545454,
            "repo_info": {
                "type": "GIT",
                "address": "https://github.com/bluez/bluez",
                "tag": "5.15",
                "version": "5.15",
                "commit": "e94fc26ea2e57b139ed2dbe0f5cd2e86d6b91b1f"
            },
            "minimum_file_matches": "508",
            "estimated_diff_files": "9"
        }
    },
    {
        "directory": "./project_name\\C",
        "match": {
            "score": 0.1,
            "repo_info": {
                "type": "GIT",
                "address": "https://github.com/ckolivas/lrzip",
                "tag": "v0.5.2",
                "version": "0.5.2",
                "commit": "91228195a7fe4040e4d1e9947054de939c7090d7"
            },
            "minimum_file_matches": "2",
            "estimated_diff_files": "27"
        }
    }
]

bom = Bom()

# преобразование данных в CycloneDX, добавление в BOM
for item in data:
    match = item['match']
    repo_info = match['repo_info']

    component = Component(
        name=repo_info['address'].split('/')[-1],  # Имя компонента из URL
        version=repo_info['version'],
        component_type=ComponentType.LIBRARY,
        purl=f"pkg:git/{repo_info['address']}@{repo_info['commit']}",
        cpe=f"cpe:2.3:a:{repo_info['address'].split('/')[-2]}:{repo_info['address'].split('/')[-1]}:{repo_info['version']}"
    )

    bom.components.add(component)

output = get_instance(bom, output_format=OutputFormat.JSON)
print(output.output_as_string())
