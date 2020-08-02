from jinja2 import Environment, FileSystemLoader
import yaml


environment = Environment(loader=FileSystemLoader('../'))
with open('../index.html', 'w') as html:
    output = (
        environment
        .get_template('template.html')
        .render(yaml.load(open('data.yml'), Loader=yaml.FullLoader))
    )
    html.write(output)
