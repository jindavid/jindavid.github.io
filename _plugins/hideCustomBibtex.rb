module Jekyll
  module HideCustomBibtex
    def hideCustomBibtex(input)
      keywords = @context.registers[:site].config['filtered_bibtex_keywords'] || []
      return input if keywords.empty?

      fields = Regexp.union(keywords.map { |keyword| Regexp.escape(keyword) })
      field_line = /^\s*(?:#{fields})\s*=/i
      input.lines.reject { |line| line.match?(field_line) }.join
    end
  end
end

Liquid::Template.register_filter(Jekyll::HideCustomBibtex)
