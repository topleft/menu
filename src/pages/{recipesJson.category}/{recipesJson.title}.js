import * as React from 'react'
import { graphql } from 'gatsby'

import Layout from '../../components/layout'

const isPdf = (image_url) => {
  try {
    return image_url.split('.').pop().toLowerCase() === 'pdf'
  }
  catch (e) {
    console.log(`Could not determine file type: ${image_url}`)
    console.log(e)
    return false
  }

}

const Recipe = ({ data: { recipesJson } }) => {
  const { title, image_urls } = recipesJson
  return (
    <Layout>
      <h2>{title}</h2>
      {
        image_urls.map((image_url) => {
          console.log(image_url)
          return isPdf(image_url) ?
            <embed
              type="application/pdf"
              src={`${image_url}?toolbar=0&navpanes=0&scrollbar=0`}
              key={image_url}
              style={{ width: "100%", height: "1000px" }} frameborder="0" /> :
            < img src={image_url} alt={title} key={image_url} />
        })
      }
    </Layout>
  )
}

export const query = graphql`
  query ($id: String) {
    recipesJson(id: { eq: $id }) {
          image_urls
          title
        }
  }
`

export default Recipe