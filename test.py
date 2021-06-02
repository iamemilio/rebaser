from rebaser import parse_cli_arguments, validate_cli_arguments
import unittest

valid_args = [
    '--source-repo', 'https://opendev.org/openstack/kuryr-kubernetes',
    '--dest-repo', 'https://github.com/openshift/kuryr-kubernetes',
    '--fork-repo', 'git@github.com:kuryr-bot/kuryr-kubernetes',
    '--working-dir', 'tmp',
    '--github-token', '/credentials/gh-key',
    '--github-key', '/credentials/gh-token',
    '--slack-webhook', '/credentials/slack-webhook',
]

invalid_url_args = [
    '--source-repo', 'opendev.org/openstack/kuryr-kubernetes',
    '--dest-repo', 'https://github/openshift/kuryr-kubernetes',
    '--fork-repo', 'git@github.com:kuryr-bot/kuryr-kubernetes',
    '--working-dir', 'tmp',
    '--github-token', '/credentials/gh-key',
    '--github-key', '/credentials/gh-token',
    '--slack-webhook', '/credentials/slack-webhook',
]

class test_cli_parser(unittest.TestCase):
    def test_valid_cli_argmuents(self):
        args, errors = parse_cli_arguments(valid_args)

        # sanity checks
        self.assertEqual(args.source_repo[0], 'https://opendev.org/openstack/kuryr-kubernetes')
        self.assertEqual(args.dest_repo[0], 'https://github.com/openshift/kuryr-kubernetes')
        self.assertEqual(args.fork_repo[0], 'git@github.com:kuryr-bot/kuryr-kubernetes')
        self.assertEqual(args.working_dir[0], 'tmp')
        self.assertEqual(args.github_token[0], '/credentials/gh-key')
        self.assertEqual(args.github_key[0], '/credentials/gh-token')
        self.assertEqual(args.slack_webhook[0], '/credentials/slack-webhook')

        # error checks
        self.assertEqual(errors, [])

    def test_invalid_url(self):
        args, errors = parse_cli_arguments(invalid_url_args)
        self.assertEqual(errors, [
            'the value for `--source-repo`, opendev.org/openstack/kuryr-kubernetes, is not a valid URL',
            'the value for `--dest-repo`, https://github/openshift/kuryr-kubernetes, is not a valid URL'
        ])

if __name__ == '__main__':
    unittest.main()
