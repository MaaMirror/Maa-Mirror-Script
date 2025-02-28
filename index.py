from src.argv import Argparser
from src import cf_test, check, issue

args = Argparser().args

token: str = args.token

if args.cf:
    api_infos = cf_test.run()
    issue.Issue(token).update_api_status(api_infos[0], api_infos[1])
if args.check:
    check.MAA(token).run()
if args.check_res:
    check.Resource(token).run()
if args.issue:
    issue.Issue(token).run()
if args.issue_res:
    issue.Issue(token).update_res()
if args.build:
    issue.Issue(token).rebuild_website()
