from concurrent import futures
import base64
import io

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):

    def Add(self, request, context):
        return lab6_pb2.AddReply(
            sum=request.a + request.b
        )

    def RawImage(self, request, context):
        image = Image.open(io.BytesIO(request.img))
        return lab6_pb2.ImageReply(
            width=image.width,
            height=image.height
        )

    def DotProduct(self, request, context):
        if len(request.a) != len(request.b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        result = sum(
            a * b for a, b in zip(request.a, request.b)
        )

        return lab6_pb2.DotProductReply(
            dotproduct=result
        )

    def JsonImage(self, request, context):
        image_data = base64.b64decode(request.img)
        image = Image.open(io.BytesIO(image_data))

        return lab6_pb2.ImageReply(
            width=image.width,
            height=image.height
        )


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Service(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

