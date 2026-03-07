# X API v2 - Python Examples

Working Python examples for the X API v2.

## Setup

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
- `xdk>=0.4.5` - X Developer Kit for Python

## Environment Variables

**For read-only operations (search, lookup):**
```bash
export BEARER_TOKEN='your_bearer_token'
```

**For user actions (post, like, repost, bookmark, mute, etc.):**
```bash
export CLIENT_ID='your_client_id'
export CLIENT_SECRET='your_client_secret'
```

**Note:** Most user action examples (create post, like, repost, bookmark, mute, block, etc.) require OAuth 2.0 authentication with `CLIENT_ID` and `CLIENT_SECRET`. Read-only examples (search, lookup) only require `BEARER_TOKEN`.

## Examples

### Posts
- `posts/create_post.py` - Create a new post (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `posts/delete_post.py` - Delete a post (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `posts/get_liking_users.py` - Get users who liked a post
- `posts/get_post_counts_all.py` - Get post counts (full archive)
- `posts/get_post_counts_recent.py` - Get post counts (recent)
- `posts/get_posts_by_ids.py` - Look up posts by ID
- `posts/get_quoted_posts.py` - Get posts that quote a post
- `posts/get_reposted_by.py` - Get users who reposted a post
- `posts/search_all.py` - Full archive search
- `posts/search_recent.py` - Recent search (last 7 days)

### Users
- `users/get_users_by_usernames.py` - Look up users by username (bearer token)
- `users/get_users_by_usernames_user_context.py` - Look up user by username (user context) (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/get_users_me.py` - Get authenticated user (me) (requires `CLIENT_ID`, `CLIENT_SECRET`)

#### User Actions - Block
- `users/block/get_blocking.py` - Get users blocked by a user (requires `CLIENT_ID`, `CLIENT_SECRET`)

#### User Actions - Bookmark
- `users/bookmark/get_bookmarks.py` - Get user's bookmarks (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/bookmark/create_bookmark.py` - Create a bookmark (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/bookmark/delete_bookmark.py` - Delete a bookmark (requires `CLIENT_ID`, `CLIENT_SECRET`)

#### User Actions - Follow
- `users/follow/get_followers.py` - Get user's followers
- `users/follow/get_following.py` - Get users a user is following

#### User Actions - Like
- `users/like/get_liked_posts.py` - Get posts liked by a user (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/like/like_post.py` - Like a post (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/like/unlike_post.py` - Unlike a post (requires `CLIENT_ID`, `CLIENT_SECRET`)

#### User Actions - Lists
- `users/lists/follow_list.py` - Follow a list (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/lists/get_followed_lists.py` - Get lists followed by a user
- `users/lists/get_list_memberships.py` - Get list memberships
- `users/lists/get_owned_lists.py` - Get lists owned by a user
- `users/lists/get_pinned_lists.py` - Get pinned lists (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/lists/pin_list.py` - Pin a list (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/lists/unfollow_list.py` - Unfollow a list (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/lists/unpin_list.py` - Unpin a list (requires `CLIENT_ID`, `CLIENT_SECRET`)

#### User Actions - Mute
- `users/mute/get_muting.py` - Get users muted by a user (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/mute/mute_user.py` - Mute a user (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/mute/unmute_user.py` - Unmute a user (requires `CLIENT_ID`, `CLIENT_SECRET`)

#### User Actions - Repost
- `users/repost/repost_post.py` - Repost a post (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `users/repost/unrepost_post.py` - Undo a repost (requires `CLIENT_ID`, `CLIENT_SECRET`)

#### User Actions - Timeline
- `users/timeline/get_mentions.py` - Get user mentions timeline
- `users/timeline/get_posts.py` - Get user's posts timeline
- `users/timeline/get_home_timeline.py` - Get home timeline (requires `CLIENT_ID`, `CLIENT_SECRET`)

### Streams
- `streams/stream_posts_filtered.py` - Filtered stream with rules
- `streams/stream_posts_sample.py` - Sampled stream

### Lists
- `lists/add_member.py` - Add member to a list (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `lists/create_list.py` - Create a new list (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `lists/delete_list.py` - Delete a list (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `lists/get_list_by_id.py` - Get list by ID
- `lists/get_list_followers.py` - Get list followers
- `lists/get_list_members.py` - Get list members
- `lists/get_list_posts.py` - Get posts from a list
- `lists/remove_member.py` - Remove member from a list (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `lists/update_list.py` - Update a list (requires `CLIENT_ID`, `CLIENT_SECRET`)

### Spaces
- `spaces/get_spaces_by_ids.py` - Look up Spaces by ID
- `spaces/search_spaces.py` - Search for Spaces

### Direct Messages
- `direct_messages/get_events_by_conversation.py` - Get DM events by conversation (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `direct_messages/get_one_to_one_conversation_events.py` - Get one-to-one conversation events (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `direct_messages/get_user_conversation_events.py` - Get user conversation events (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `direct_messages/post_dm_to_conversation.py` - Post DM to conversation (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `direct_messages/post_group_conversation_dm.py` - Post group conversation DM (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `direct_messages/post_one_to_one_dm.py` - Post one-to-one DM (requires `CLIENT_ID`, `CLIENT_SECRET`)

### Media
- `media/media_upload_v2.py` - Media upload v2 (requires `CLIENT_ID`, `CLIENT_SECRET`)
- `media/upload.py` - Media upload (requires `CLIENT_ID`, `CLIENT_SECRET`)

### Compliance
- `compliance/create_jobs.py` - Create compliance job
- `compliance/download_results.py` - Download compliance results
- `compliance/get_jobs_by_id.py` - Get compliance job by ID
- `compliance/get_jobs.py` - Get compliance jobs
- `compliance/upload_ids.py` - Upload IDs for compliance

### Usage
- `usage/get_usage.py` - Get API usage information

## Running Examples

```bash
# Make sure environment variables are set
python posts/search_recent.py
```

## More Information

- [X API Documentation](https://developer.x.com/en/docs/twitter-api)
- [X Developer Portal](https://developer.x.com/en/portal/dashboard)
