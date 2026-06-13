import argparse

from resume_q_a.app import describe_project, generate_response


def main() -> None:
    parser = argparse.ArgumentParser(description=describe_project())
    parser.add_argument("prompt", nargs="*", help="Request for the assistant")
    args = parser.parse_args()
    prompt = " ".join(args.prompt) or "Create a first useful workflow"
    print(generate_response(prompt))


if __name__ == "__main__":
    main()
