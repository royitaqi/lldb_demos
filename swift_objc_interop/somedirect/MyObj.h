#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface MyObj : NSObject

@property (readwrite, direct) NSInteger directProp;
@property (nonatomic, readonly, direct) NSInteger anotherDirectProp;

@end

NS_ASSUME_NONNULL_END
