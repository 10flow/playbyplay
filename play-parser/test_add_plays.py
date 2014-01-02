import unittest
from add_plays import parse_args


class TestPlayParsing(unittest.TestCase):

    def test_args(self):
        raw_args = 'input.csv dbstring'.split(' ')
        args = parse_args(raw_args)
        print(args)
        self.assertFalse(args.outputfiletype)
        self.assertEquals(1, len(args.infiles))
        self.assertEquals('input.csv', args.infiles[0])
        self.assertEquals('dbstring', args.output)

        raw_args = '1.csv 2.csv 3.csv dbstring'.split(' ')
        args = parse_args(raw_args)
        print(args)
        self.assertFalse(args.outputfiletype)
        self.assertEquals(3, len(args.infiles))
        self.assertEquals('dbstring', args.output)

        raw_args = '--outputfile=csv input.csv out.csv'.split(' ')
        args = parse_args(raw_args)
        print(args)
        self.assertEquals('csv', args.outputfiletype)
        self.assertEquals('input.csv', args.infiles[0])
        self.assertEquals('out.csv', args.output)

        raw_args = '-f json input.csv out.csv'.split(' ')
        args = parse_args(raw_args)
        print(args)
        self.assertEquals('json', args.outputfiletype)


if __name__ == '__main__':
    unittest.main()