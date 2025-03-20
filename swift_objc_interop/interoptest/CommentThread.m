#import "CommentThread.h"

#import "MyObj.h"

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

  MyObj *x = [[MyObj alloc] init];
  NSLog(@"%p", x);

  return self; // breakpoint here to stop in Objective-C
}

@end
