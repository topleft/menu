/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.com/docs/how-to/querying-data/use-static-query/
 */

import * as React from "react"
import { useStaticQuery, graphql } from 'gatsby'
import Header from "./header"
import Navigation from "./navigation"
import "./layout.css"

const Layout = ({ children }) => {
  const categories = useStaticQuery(
    graphql`
      query Categories {
        allRecipesJson(sort: {category: ASC}, filter: {category: {ne: "other"}}) {
          distinct(field: {category: SELECT})
        }
      }
    `
  )
  const pageLinks = categories.allRecipesJson.distinct.map((category) => {
    return category !== 'other' && { path: `/${category}`, label: category }
  })
  pageLinks.push({ path: '/other', label: 'other' })

  return (
    <>
      <Header siteTitle={`Recipes`} />
      <div
        style={{
          margin: `0 auto`,
          maxWidth: `var(--size-content)`,
          padding: `var(--size-gutter)`,
        }}
      >
        <Navigation pageLinks={pageLinks} />
        <main>{children}</main>
        <footer
          style={{
            marginTop: `var(--space-5)`,
            fontSize: `var(--font-sm)`,
          }}
        >
          Built by
          {` `}
          <a href="https://www.topleft.dev">topleft</a>
        </footer>
      </div>
    </>
  )
}

export default Layout
