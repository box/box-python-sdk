# AuthorizationManager

- [Authorize user](#authorize-user)
- [Request access token](#request-access-token)
- [Refresh access token](#refresh-access-token)
- [Revoke access token](#revoke-access-token)

## Authorize user

Authorize a user by sending them through the [Box](https://box.com)
website and request their permission to act on their behalf.

This is the first step when authenticating a user using
OAuth 2.0. To request a user's authorization to use the Box APIs
on their behalf you will need to send a user to the URL with this
format.

This operation is performed by calling function `authorize_user`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-authorize/).

_Currently we don't have an example for calling `authorize_user` in integration tests_

### Arguments

- response_type `AuthorizeUserResponseType`
  - The type of response we'd like to receive.
- client_id `str`
  - The Client ID of the application that is requesting to authenticate the user. To get the Client ID for your application, log in to your Box developer console and click the **Edit Application** link for the application you're working with. In the OAuth 2.0 Parameters section of the configuration page, find the item labelled `client_id`. The text of that item is your application's Client ID.
- redirect_uri `Optional[str]`
  - The URI to which Box redirects the browser after the user has granted or denied the application permission. This URI match one of the redirect URIs in the configuration of your application. It must be a valid HTTPS URI and it needs to be able to handle the redirection to complete the next step in the OAuth 2.0 flow. Although this parameter is optional, it must be a part of the authorization URL if you configured multiple redirect URIs for the application in the developer console. A missing parameter causes a `redirect_uri_missing` error after the user grants application access.
- state `Optional[str]`
  - A custom string of your choice. Box will pass the same string to the redirect URL when authentication is complete. This parameter can be used to identify a user on redirect, as well as protect against hijacked sessions and other exploits.
- scope `Optional[str]`
  - A space-separated list of application scopes you'd like to authenticate the user for. This defaults to all the scopes configured for the application in its configuration page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Does not return any data, but rather should be used in the browser.

## Request access token

Request an Access Token using either a client-side obtained OAuth 2.0
authorization code or a server-side JWT assertion.

An Access Token is a string that enables Box to verify that a
request belongs to an authorized session. In the normal order of
operations you will begin by requesting authentication from the
[authorize](#get-authorize) endpoint and Box will send you an
authorization code.

You will then send this code to this endpoint to exchange it for
an Access Token. The returned Access Token can then be used to to make
Box API calls.

This operation is performed by calling function `request_access_token`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-oauth2-token/).

_Currently we don't have an example for calling `request_access_token` in integration tests_

### Arguments

- grant_type `RequestAccessTokenGrantType`
  - The type of request being made, either using a client-side obtained authorization code, a refresh token, a JWT assertion, client credentials grant or another access token for the purpose of downscoping a token.
- client_id `Optional[str]`
  - The Client ID of the application requesting an access token. Used in combination with `authorization_code`, `client_credentials`, or `urn:ietf:params:oauth:grant-type:jwt-bearer` as the `grant_type`.
- client_secret `Optional[str]`
  - The client secret of the application requesting an access token. Used in combination with `authorization_code`, `client_credentials`, or `urn:ietf:params:oauth:grant-type:jwt-bearer` as the `grant_type`.
- code `Optional[str]`
  - The client-side authorization code passed to your application by Box in the browser redirect after the user has successfully granted your application permission to make API calls on their behalf. Used in combination with `authorization_code` as the `grant_type`.
- refresh_token `Optional[str]`
  - A refresh token used to get a new access token with. Used in combination with `refresh_token` as the `grant_type`.
- assertion `Optional[str]`
  - A JWT assertion for which to request a new access token. Used in combination with `urn:ietf:params:oauth:grant-type:jwt-bearer` as the `grant_type`.
- subject_token `Optional[str]`
  - The token to exchange for a downscoped token. This can be a regular access token, a JWT assertion, or an app token. Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange` as the `grant_type`.
- subject_token_type `Optional[RequestAccessTokenSubjectTokenType]`
  - The type of `subject_token` passed in. Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange` as the `grant_type`.
- actor_token `Optional[str]`
  - The token used to create an annotator token. This is a JWT assertion. Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange` as the `grant_type`.
- actor_token_type `Optional[RequestAccessTokenActorTokenType]`
  - The type of `actor_token` passed in. Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange` as the `grant_type`.
- scope `Optional[str]`
  - The space-delimited list of scopes that you want apply to the new access token. The `subject_token` will need to have all of these scopes or the call will error with **401 Unauthorized**..
- resource `Optional[str]`
  - Full URL for the file that the token should be generated for.
- box_subject_type `Optional[RequestAccessTokenBoxSubjectType]`
  - Used in combination with `client_credentials` as the `grant_type`.
- box_subject_id `Optional[str]`
  - Used in combination with `client_credentials` as the `grant_type`. Value is determined by `box_subject_type`. If `user` use user ID and if `enterprise` use enterprise ID.
- box_shared_link `Optional[str]`
  - Full URL of the shared link on the file or folder that the token should be generated for.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AccessToken`.

Returns a new Access Token that can be used to make authenticated
API calls by passing along the token in a authorization header as
follows `Authorization: Bearer <Token>`.

## Refresh access token

Refresh an Access Token using its client ID, secret, and refresh token.

This operation is performed by calling function `refresh_access_token`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-oauth2-token--refresh/).

_Currently we don't have an example for calling `refresh_access_token` in integration tests_

### Arguments

- grant_type `RefreshAccessTokenGrantType`
  - The type of request being made, in this case a refresh request.
- client_id `str`
  - The client ID of the application requesting to refresh the token.
- client_secret `str`
  - The client secret of the application requesting to refresh the token.
- refresh_token `str`
  - The refresh token to refresh.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AccessToken`.

Returns a new Access Token that can be used to make authenticated
API calls by passing along the token in a authorization header as
follows `Authorization: Bearer <Token>`.

## Revoke access token

Revoke an active Access Token, effectively logging a user out
that has been previously authenticated.

This operation is performed by calling function `revoke_access_token`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-oauth2-revoke/).

_Currently we don't have an example for calling `revoke_access_token` in integration tests_

### Arguments

- client_id `Optional[str]`
  - The Client ID of the application requesting to revoke the access token.
- client_secret `Optional[str]`
  - The client secret of the application requesting to revoke an access token.
- token `Optional[str]`
  - The access token to revoke.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the token was successfully revoked.
