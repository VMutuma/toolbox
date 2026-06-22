import type { StructureResolver } from 'sanity/structure';

// https://www.sanity.io/docs/structure-builder-cheat-sheet
export const structure: StructureResolver = (S) =>
  S.list()
    .title('Content')
    .items([
      S.documentTypeListItem('careers').title('Careers'),
      S.documentTypeListItem('nextgen').title('Nextgen'),
      S.documentTypeListItem('casestudy').title('Case studies'),
      S.documentTypeListItem('blog').title('Blogs'),
      S.divider(),
      ...S.documentTypeListItems().filter(
        (item) =>
          item.getId() &&
          ![
            'post',
            'category',
            'author',
            'careers',
            'nextgen',
            'casestudy',
            'blog',
          ].includes(item.getId()!)
      ),
    ]);
