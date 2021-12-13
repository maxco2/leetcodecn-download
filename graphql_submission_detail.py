gql_body = '''query mySubmissionDetail($id: ID!) {
  submissionDetail(submissionId: $id) {
    id
    code
    runtime
    memory
    rawMemory
    statusDisplay
    timestamp
    lang
    passedTestCaseCnt
    totalTestCaseCnt
    sourceUrl
    question {
      titleSlug
      title
      translatedTitle
      questionId
      __typename
    }
    ... on GeneralSubmissionNode {
      outputDetail {
        codeOutput
        expectedOutput
        input
        compileError
        runtimeError
        lastTestcase
        __typename
      }
      __typename
    }
    submissionComment {
      comment
      flagType
      __typename
    }
    __typename
  }
}
'''
gql = '''{"operationName": "mySubmissionDetail", "variables": {"id": "%s"}, "query": "%s"}'''


def get_submission_detail_gql(problem_id: str):
    return gql % (problem_id, repr(gql_body)[1:-1])


__all__ = ["get_submission_detail_gql"]

if __name__ == '__main__':
    import json
    print(get_submission_detail_gql("213"))

