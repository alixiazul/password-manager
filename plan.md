- utility functions
  - valid user input
  - store secret
  - list secrets
  - retrieve secrets
  - delete secret

the secret will look like this
{"bidenj":"Pa55word"}

{'ARN': 'arn:aws:secretsmanager:eu-west-2:123456789012:secret:MyTestSecret-ZpUlCs', 'Name': 'MyTestSecret', 'VersionId': '45b7ecdd-c190-4874-b8e5-c80933c0da8f', 'ResponseMetadata': {'RequestId': 'R2mMOdTd0H7DAiJs7yAzfquG2tsRCWvvUIhLixerabNNxxmJPL1u', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'amazon.com', 'date': 'Thu, 09 May 2024 11:07:48 GMT', 'x-amzn-requestid': 'R2mMOdTd0H7DAiJs7yAzfquG2tsRCWvvUIhLixerabNNxxmJPL1u'}, 'RetryAttempts': 0}}
{'SecretList': [{'ARN': 'arn:aws:secretsmanager:eu-west-2:123456789012:secret:MyTestSecret-ZpUlCs', 'Name': 'MyTestSecret', 'Description': 'This is just a test fot the firt boto', 'LastChangedDate': datetime.datetime(2024, 5, 9, 11, 7, 48, tzinfo=tzlocal()), 'SecretVersionsToStages': {'45b7ecdd-c190-4874-b8e5-c80933c0da8f': ['AWSCURRENT']}, 'CreatedDate': datetime.datetime(2024, 5, 9, 11, 7, 48, tzinfo=tzlocal())}], 'ResponseMetadata': {'RequestId': '9LB06QDtwfQ5X82ITRPIcBnK7fbzzi9NYoDu7XiqNVuH0BGXmTga', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'amazon.com', 'date': 'Thu, 09 May 2024 11:07:48 GMT', 'x-amzn-requestid': '9LB06QDtwfQ5X82ITRPIcBnK7fbzzi9NYoDu7XiqNVuH0BGXmTga'}, 'RetryAttempts': 0}}

{'ARN': 'arn:aws:secretsmanager:eu-west-2:123456789012:secret:MyTestSecret-iZBGMI', 'Name': 'MyTestSecret', 'VersionId': '964221af-3945-4de7-a336-eba7238dd08e', 'ResponseMetadata': {'RequestId': 'utlEFBzb16ppq6v1qQVFQDFy4DJP2ksXQKMCujKT23VGlROEyWKQ', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'amazon.com', 'date': 'Thu, 09 May 2024 11:10:41 GMT', 'x-amzn-requestid': 'utlEFBzb16ppq6v1qQVFQDFy4DJP2ksXQKMCujKT23VGlROEyWKQ'}, 'RetryAttempts': 0}}
{'SecretList': [{'ARN': 'arn:aws:secretsmanager:eu-west-2:123456789012:secret:MyTestSecret-iZBGMI', 'Name': 'MyTestSecret', 'Description': 'This is just a test fot the firt boto', 'LastChangedDate': datetime.datetime(2024, 5, 9, 11, 10, 41, tzinfo=tzlocal()), 'SecretVersionsToStages': {'964221af-3945-4de7-a336-eba7238dd08e': ['AWSCURRENT']}, 'CreatedDate': datetime.datetime(2024, 5, 9, 11, 10, 41, tzinfo=tzlocal())}], 'ResponseMetadata': {'RequestId': 'R40V4Jz2LZmyIhTKTHEgcDIWOmdCa28s2y3EuT6odDCE1fS2fPgx', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'amazon.com', 'date': 'Thu, 09 May 2024 11:10:41 GMT', 'x-amzn-requestid': 'R40V4Jz2LZmyIhTKTHEgcDIWOmdCa28s2y3EuT6odDCE1fS2fPgx'}, 'RetryAttempts': 0}}
