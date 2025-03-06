#import <Foundation/Foundation.h>

#import "CommentModel.h"
#import "EmojiModel.h"

NS_ASSUME_NONNULL_BEGIN

/**
 * Class summary
 */
@interface CommentThread : NSObject

@property (nullable, nonatomic, readonly) CommentModel *caption;
@property (nonatomic, readonly) NSArray<CommentModel *> *comments;
@property (nullable, nonatomic, readonly, copy, direct) NSArray<EmojiModel *> *quickResponseEmojis;
@property (nonatomic, readonly, direct) NSInteger threadsCommentCount;

@end

NS_ASSUME_NONNULL_END
