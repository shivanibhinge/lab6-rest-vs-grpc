import argparse
import base64
import random
import time

import grpc

import lab6_pb2
import lab6_pb2_grpc


IMAGE_FILE = "Flatirons_Winter_Sunrise_edit_2.jpg"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("host")
    parser.add_argument(
        "operation",
        choices=["add", "rawImage", "dotProduct", "jsonImage"]
    )
    parser.add_argument("repetitions", type=int)
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    if args.repetitions <= 0:
        parser.error("Repetitions must be positive")

    with open(IMAGE_FILE, "rb") as f:
        image_data = f.read()

    encoded_image = base64.b64encode(
        image_data
    ).decode("utf-8")

    with grpc.insecure_channel(
        f"{args.host}:50051"
    ) as channel:

        stub = lab6_pb2_grpc.Lab6ServiceStub(channel)
        grpc.channel_ready_future(channel).result(timeout=15)

        start = time.perf_counter()

        for _ in range(args.repetitions):

            if args.operation == "add":
                response = stub.Add(
                    lab6_pb2.AddRequest(a=5, b=10)
                )

            elif args.operation == "rawImage":
                response = stub.RawImage(
                    lab6_pb2.RawImageRequest(
                        img=image_data
                    )
                )

            elif args.operation == "dotProduct":
                a = [
                    random.random()
                    for _ in range(100)
                ]
                b = [
                    random.random()
                    for _ in range(100)
                ]

                response = stub.DotProduct(
                    lab6_pb2.DotProductRequest(
                        a=a, b=b
                    )
                )

            elif args.operation == "jsonImage":
                response = stub.JsonImage(
                    lab6_pb2.JsonImageRequest(
                        img=encoded_image
                    )
                )

            if args.debug:
                print(response)

        elapsed = time.perf_counter() - start
        average_ms = elapsed * 1000 / args.repetitions

        print(
            f"Running {args.repetitions} reps "
            f"against {args.host}:50051"
        )
        print(
            f"Took {average_ms:.6f} ms per operation"
        )


if __name__ == "__main__":
    main()
