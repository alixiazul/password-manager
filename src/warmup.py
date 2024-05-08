import logging
import boto3
from botocore.exceptions import ClientError
import os

BUCKET_NAME = "nc-ar-fo-password-manager"
FILE1 = "./src/file1.txt"
FILE2 = "./src/file2.txt"


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client("s3")
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client("s3", region_name=region)
            location = {"LocationConstraint": region}
            s3_client.create_bucket(
                Bucket=bucket_name, CreateBucketConfiguration=location
            )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def listing_buckets():
    # Retrieve the list of existing buckets
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    # Return the bucket names
    return [bucket["Name"] for bucket in response["Buckets"]]


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_objects(bucket):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    print([obj.key for obj in bucket.objects.all()])
    return [obj.key for obj in bucket.objects.all()]


def read_object(filename, bucket):
    # Getting the object:
    s3 = boto3.client("s3")
    print("Getting S3 object...")
    response = s3.get_object(Bucket=bucket, Key=filename)
    print("Done, response body:")
    print(response["Body"].read())


def delete_objects(bucket):
    s3 = boto3.client("s3")
    objects = list_objects(bucket)

    s3.delete_objects(
        Bucket=bucket,
        Delete={"Objects": [{"Key": obj} for obj in objects], "Quiet": True},
    )


def delete_bucket(bucket):
    s3 = boto3.resource("s3")
    bucket_resource = s3.Bucket(bucket)
    bucket_resource.delete()


if __name__ == "__main__":
    create_bucket(BUCKET_NAME, "eu-west-2")
    upload_file(FILE1, BUCKET_NAME, "file1.txt")
    upload_file(FILE2, BUCKET_NAME, "file2.txt")
    list_objects(BUCKET_NAME)
    read_object("file1.txt", BUCKET_NAME)
    delete_objects(BUCKET_NAME)
    delete_bucket(BUCKET_NAME)
    listing_buckets()
