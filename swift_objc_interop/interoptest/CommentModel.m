#import "CommentModel.h"

@implementation CommentModel

- (instancetype)init
{
  if (self = [super init]) {
      self.user = @"some user";
  }
  return self;
}

@end
