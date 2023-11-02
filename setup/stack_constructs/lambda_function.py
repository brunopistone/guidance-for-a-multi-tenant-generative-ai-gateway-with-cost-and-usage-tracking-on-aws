from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambda_,
    Duration,
)

class LambdaFunction(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        role: str,
        provisioned_concurrency: int = None,
    ):
        super().__init__(scope, id)

        self.id = id
        self.role = role
        self.provisioned_concurrency = provisioned_concurrency

    def build(
            self,
            function_name: str,
            code_dir: str,
            environment: dict,
            memory: int,
            timeout: int,
            layers: list = [],
    ):
        fn = lambda_.Function(
            self,
            id=f"{self.id}_{function_name}_function",
            function_name=function_name,
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="index.lambda_handler",
            code=lambda_.Code.from_asset(code_dir),
            timeout=Duration.seconds(timeout),
            memory_size=memory,
            environment=environment,
            layers=layers,
            role=iam.Role.from_role_name(self, f"{self.id}_{function_name}_role", self.role)
        )

        return fn