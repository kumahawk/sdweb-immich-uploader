from modules import prompt_parser, shared

def prompt_to_tags(p):
    use_prompt_parser = shared.opts.use_prompt_parser_when_save_prompt_to_immich_as_tags

    if use_prompt_parser:
        return [ x[0].strip() for x in prompt_parser.parse_prompt_attention(p) ]
    else:
        return [ x.strip() for x in p.split(",") if x.strip() != "" ]