import * as React from "react"
import { Link } from "gatsby"

const PageLink = ({ link }) => {
  return (
    <li
      style={{
        'padding': 'var(--space-4) var(--size-gutter)'
      }}>
      <Link to={link.path}>{link.label}</Link>
    </li>
  )
}

export default function Navigation({ pageLinks }) {
  return (
    <div>
      <ul style={{
        display: "flex",
        padding: "10px",
        listStyle: "none"
      }}>
        {
          pageLinks.map((link) =>
            <PageLink link={link} key={`${link.label}-link`} />
          )
        }
      </ul>
    </div>
  )
}