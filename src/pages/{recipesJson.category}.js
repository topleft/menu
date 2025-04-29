import * as React from 'react'
import { graphql, Link } from 'gatsby'

import Layout from '../components/layout'

const RecipeLink = ({ slug, title }) => {
  return (
    <li>
      <Link to={slug}>{title}</Link>
    </li>
  )
}

const RecipeIndex = ({ data }) => {
  const recipes = data.allRecipesJson.edges
  return (
    <Layout>
      <ul>
        {recipes.map((recipe) => {
          return <RecipeLink {...recipe.node} key={recipe.node.id} />
        })}
      </ul>
    </Layout>
  )
}

export const query = graphql`
  query ($category: String) {
    allRecipesJson(filter: {category: {eq: $category}}) {
      edges {
        node {
          category
          title
          slug
          id
        }
      }
    }
  }
`

export default RecipeIndex