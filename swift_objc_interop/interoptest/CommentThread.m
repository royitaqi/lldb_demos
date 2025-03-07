#import "CommentThread.h"

@implementation CommentThread

- (instancetype)init
{
  if (self = [super init]) {
      _caption = [[CommentModel alloc] init];
      _comments = @[
          [[CommentModel alloc] init],
          [[CommentModel alloc] init]
      ];
      _quickResponseEmojis = @[
          [[EmojiModel alloc] init],
          [[EmojiModel alloc] init],
      ];
      _threadsCommentCount = 123;
  }
  return self; // breakpoint here to stop in Objective-C
}

@end
