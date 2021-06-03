from rebaser import commit_go_mod_updates, parse_cli_arguments, validate_cli_arguments
import unittest
import os
from git import Repo

valid_args = [
    '--source-repo', 'https://opendev.org/openstack/kuryr-kubernetes',
    '--dest-repo', 'https://github.com/openshift/kuryr-kubernetes',
    '--fork-repo', 'git@github.com:kuryr-bot/kuryr-kubernetes',
    '--working-dir', 'tmp',
    '--github-token', '/credentials/gh-key',
    '--github-key', '/credentials/gh-token',
    '--slack-webhook', '/credentials/slack-webhook',
    '--update-go-modules',
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
        self.assertEqual(args.update_go_modules, True)

        # error checks
        self.assertEqual(errors, [])

    def test_invalid_url(self):
        args, errors = parse_cli_arguments(invalid_url_args)
        self.assertEqual(errors, [
            'the value for `--source-repo`, opendev.org/openstack/kuryr-kubernetes, is not a valid URL',
            'the value for `--dest-repo`, https://github/openshift/kuryr-kubernetes, is not a valid URL'
        ])

class go_mod_test(unittest.TestCase):
    def test_update_and_commit(self):
        working_dir = os.getcwd()
        tmp_dir = os.path.join(os.getcwd(), "tmp")
        test_file = os.path.join(tmp_dir, "test.go")
        script = '''
package main

import (
	"k8s.io/klog/v2"
)

func main() {
	klog.Errorln("This is a test")
	return
}
'''

        # Create testing directory and files
        os.mkdir(tmp_dir)
        f = open(test_file, "x")
        f.write(script)
        f.close()
        repo = Repo.init(tmp_dir)

        os.chdir(tmp_dir)
        os.system("go mod init")

        try:
            commit_go_mod_updates(repo)
        except Exception as err:
            self.assertEqual(str(err), "")
        else:
            commits = list(repo.iter_commits())
            self.assertEqual(len(commits), 1)
            self.assertEqual(commits[0].message, "Updating and vendoring go modules after an upstream merge.\n")
        finally:
            # clean up
            os.chdir(working_dir)
            os.system("rm -rf " + str(tmp_dir))

if __name__ == '__main__':
    unittest.main()
