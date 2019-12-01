## Configルールで違反時にSNSを通じてメール及びLambda通知

###Q. Lambdaの実行ログがCWLロググループに吐かれない
------------------------------------------------------------
A. Lambdaの実行IAMロールにCWLadminポリシーがない


###Q, ConfigRuleをトリガーにSNSトピックが動かない
------------------------------------------------------------
A. SNStopicのアクセスポリシーにConfigからのPublish権を与えて
{
    "Sid": "configRuleToSNS_publish",
    "Effect": "Allow",
    "Principal": {
        "AWS": "<<ConfigのIAMロールARN値>>"
    },
    "Action": "SNS.Publish",
    "Resource": "<<SNSのトピックARN値>>"
}
