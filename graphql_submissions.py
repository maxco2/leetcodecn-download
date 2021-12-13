import sys

gql_body = '''
query submissions($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $markedOnly: Boolean, $lang: String) {
  submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug, markedOnly: $markedOnly, lang: $lang) {
    lastKey
    hasNext
    submissions {
      id
      statusDisplay
      lang
      runtime
      timestamp
      url
      isPending
      memory
      submissionComment {
        comment
        flagType
        __typename
      }
      __typename
    }
    __typename
  }
}
'''
gql = '''{"query":"%s","variables":{"offset":0,"limit":40,"lastKey":null,"questionSlug":%s}}'''
gql_py = '''{"query":"%s","variables":{"offset":0,"limit":40,"lastKey":null,"questionSlug":"%s"}}'''


def get_submission_gql(question_slug: str):
    return gql_py % (repr(gql_body)[1:-1], question_slug)


__all__ = ["get_submission_gql"]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(gql % (repr(gql_body)[1:-1], sys.argv[1]))
