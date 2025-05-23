#let project(
  title: "",
  author: "",
  body,
) = {
  // Set document metadata
  set document(author: author, title: title)
  set page(
    numbering: "1",
    number-align: center,
  )
  
  // Configure heading spacing and numbering
  set heading(
    numbering: "1.1",
  )
  show heading: it => {
    // Add space before heading
    v(1.5em)
    it
  }
  
  // Title page
  align(center)[
    #image("assets\logo_zucchetti.png", width: 60%)
    #v(15em)
    #block(text(weight: 700, size: 32pt)[#title])
    #v(4em)
    #block(text(weight: 300, size: 20pt)[Gini])
    #v(0.5em)
    #block(text(weight: 300, size: 20pt)[
      Integrazione di LLM in Git lato versionamento
    ])
    #v(2em)
    #block(text(size: 12pt)[#author])
  ]

  // Start main content on new page
  pagebreak()
  
  // Table of contents
  outline(
    title: "Indice",
    indent: 2em
  )

  // Start main content on new page
  pagebreak()
  
  // Main body content
  set par(justify: true)
  body
}