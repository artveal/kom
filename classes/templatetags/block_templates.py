from django import template
from ..managers import OthersManager

register = template.Library()

# News block
@register.inclusion_tag('blocks/news-block.html', takes_context=True)
def news_block(context):
    news = OthersManager.NewsManager().getLatestNews()
    return {"news": news}

# World map block.
@register.inclusion_tag('blocks/worldmap-block.svg', takes_context=True)
def worldmap_block(context, default_nations=True):
    nations = OthersManager.NationsManager().getAllNations()
    return {"nations": nations, "use_default_nations": default_nations}