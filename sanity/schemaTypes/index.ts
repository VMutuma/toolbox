import { type SchemaTypeDefinition } from 'sanity';

import { blockContentType } from './blockContentType';
import { careers } from './careers';
import { nextgen } from './nextgen';
import { blog } from './blog';
import { casestudy } from './casestudy';

export const schema: { types: SchemaTypeDefinition[] } = {
  types: [blockContentType, careers, nextgen, blog, casestudy],
};
