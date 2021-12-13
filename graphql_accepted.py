import sys

gql_body = '''
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    hasMore
    total
    questions {
      acRate
      difficulty
      freqBar
      frontendQuestionId
      isFavor
      paidOnly
      solutionNum
      status
      title
      titleCn
      titleSlug
      topicTags {
        name
        nameTranslated
        id
        slug
      }
      extra {
        hasVideoSolution
        topCompanyTags {
          imgUrl
          slug
          numSubscribed
        }
      }
    }
  }
}
'''
gql = '''{"query":"%s","variables":{"categorySlug":"","skip":%s,"limit":150,"filters":{"status":"AC"}}}'''


def get_accepted_gql(skip: str):
    return gql % (repr(gql_body)[1:-1], skip)


__all__ = ["get_accepted_gql"]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(gql % (repr(gql_body)[1:-1], sys.argv[1]))
    else:
        print(gql % (repr(gql_body)[1:-1], '0'))
