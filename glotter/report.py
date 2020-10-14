import csv
import sys

from glotter.source import get_sources
from glotter.settings import Settings


def _error_and_exit(msg):
    print(msg)
    sys.exit(1)


def report(args):
    filepath = args.output

    projects = sorted([p.display_name for p in Settings().projects.values()])
    language_stats = _collect_language_stats(projects)
    languages = sorted(language_stats.keys())

    if filepath is not None:
        _write_csv(language_stats, projects, filepath)
    else:
        _write_stdout(language_stats, projects, languages)


def _get_project_display_name(key):
    return Settings().projects[key].display_name


def _write_csv(language_stats, projects, filepath=None):
    filepath = filepath or 'glotter-report.csv'
    with open(filepath, 'w', newline='') as csv_file:
        languages = sorted(language_stats.keys())
        projects = ['Name'] + projects
        writer = csv.DictWriter(csv_file, fieldnames=projects)
        writer.writeheader()
        for language in languages:
            writer.writerow(language_stats[language])
        print(f'Report written to {filepath}')


def _collect_language_stats(projects):
    language_stats = {}
    sources_by_type = get_sources(Settings().source_root)

    for project, sources in sources_by_type.items():
        display_name = _get_project_display_name(project)
        for source in sources:
            if source.language not in language_stats:
                language_stats[source.language] = {p: '' for p in projects}
                language_stats[source.language]['name'] = source.language
            language_stats[source.language][display_name] = f'{source.name}{source.extension}'

    return language_stats


def _write_stdout(language_stats, projects, languages):
    column_widths = _get_column_widths(language_stats, projects, languages)
    lang_width = max([len(lang) for lang in languages])

    header_line = f'| {{0:<{lang_width}}} | '.format('Language')
    header_underline = f'| ' + ('-' * lang_width) + ' | '
    column_template = f'| {{name:<{lang_width}}} | '
    for project in projects:
        header_line += f'{{0:<{column_widths[project]}}} | '.format(project)
        header_underline += ('-' * column_widths[project]) + ' | '
        column_template += f'{{{project}:<{column_widths[project]}}} | '

    print(header_line)
    print(header_underline)
    for lang in languages:
        print(column_template.format(**language_stats[lang]))


def _get_column_widths(language_stats, projects, languages):
    column_widths = {}
    for project in projects:
        max_len = len(project)
        for lang in languages:
            if project in language_stats[lang]:
                entry_len = len(language_stats[lang][project])
                if entry_len > max_len:
                    max_len = entry_len

        column_widths[project] = max_len
    return column_widths
