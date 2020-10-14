import csv
import sys

from glotter.source import get_sources
from glotter.settings import Settings


def _error_and_exit(msg):
    print(msg)
    sys.exit(1)


def report(args):
    filepath = args.output
    reporter = Reporter()
    if filepath is not None:
        reporter.write_csv(filepath)
    else:
        reporter.write_stdout()


class Reporter:
    def __init__(self):
        self._projects = sorted([p.display_name for p in Settings().projects.values()])
        self._language_stats = self._collect_language_stats()
        self._languages = sorted(self._language_stats.keys())

    @staticmethod
    def _get_project_display_name(key):
        return Settings().projects[key].display_name

    def _collect_language_stats(self):
        language_stats = {}
        sources_by_type = get_sources(Settings().source_root)

        for project, sources in sources_by_type.items():
            display_name = self._get_project_display_name(project)
            for source in sources:
                if source.language not in language_stats:
                    language_stats[source.language] = {p: '' for p in self._projects}
                    language_stats[source.language]['Name'] = source.language
                language_stats[source.language][display_name] = f'{source.name}{source.extension}'

        return language_stats

    def write_csv(self, filepath=None):
        filepath = filepath or 'glotter-report.csv'
        with open(filepath, 'w', newline='') as csv_file:
            languages = sorted(self._language_stats.keys())
            projects = ['Name'] + self._projects
            writer = csv.DictWriter(csv_file, fieldnames=projects)
            writer.writeheader()
            for language in languages:
                writer.writerow(self._language_stats[language])
            print(f'Report written to {filepath}')

    def write_stdout(self):
        column_widths = self._get_column_widths()
        lang_width = max([len(lang) for lang in self._languages])

        header_line = f'| {{0:<{lang_width}}} | '.format('Language')
        header_underline = f'| ' + ('-' * lang_width) + ' | '
        column_template = f'| {{Name:<{lang_width}}} | '
        for project in self._projects:
            header_line += f'{{0:<{column_widths[project]}}} | '.format(project)
            header_underline += ('-' * column_widths[project]) + ' | '
            column_template += f'{{{project}:<{column_widths[project]}}} | '

        print(header_line)
        print(header_underline)
        for lang in self._languages:
            print(column_template.format(**self._language_stats[lang]))

    def _get_column_widths(self):
        column_widths = {}
        for project in self._projects:
            max_len = len(project)
            for lang in self._languages:
                if project in self._language_stats[lang]:
                    entry_len = len(self._language_stats[lang][project])
                    if entry_len > max_len:
                        max_len = entry_len

            column_widths[project] = max_len
        return column_widths
